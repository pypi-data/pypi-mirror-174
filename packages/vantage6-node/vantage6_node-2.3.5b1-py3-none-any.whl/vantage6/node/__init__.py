""" Node

A node in its simplest would retrieve a task from the central server by
an API call, run this task and finally return the results to the central
server again.

The node application is seperated in 4 threads:
- main thread, waits for new tasks to be added to the queue and
    run the tasks
- listening thread, listens for incommin websocket messages. Which
    are handled by NodeTaskNamespace.
- speaking thread, waits for results from docker to return and posts
    them at the central server
- proxy server thread, provides an interface for master containers
    to post tasks and retrieve results
"""
import sys
import os
import random
import time
import datetime
import logging
import queue
import shutil
import json

from pathlib import Path
from threading import Thread
# from socketIO_client import SocketIO, SocketIONamespace
from socketio import (
    ClientNamespace,
    Client as SocketIO
)
from gevent.pywsgi import WSGIServer

from . import globals as cs

from vantage6.common.docker_addons import ContainerKillListener
from vantage6.node.docker_manager import DockerManager
from vantage6.node.server_io import NodeClient
from vantage6.node import proxy_server
from vantage6.node.util import logger_name


class NodeTaskNamespace(ClientNamespace):
    """Class that handles incoming websocket events."""

    # reference to the node objects, so a callback can edit the
    # node instance.
    node_worker_ref = None

    def __init__(self, *args, **kwargs):
        """ Handler for a websocket namespace.
        """
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger(logger_name(__name__))

    def on_connect(self):
        """On connect or reconnect"""
        self.log.info('Reconnected to the server')
        self.node_worker_ref.sync_task_queue_with_server()
        self.log.debug("Tasks synced again with the server...")

    def on_message(self, data):
        self.log.info(data)

    def on_disconnect(self):
        """ Server disconnects event."""
        # self.node_worker_ref.socketIO.disconnect()
        self.log.info('Disconnected from the server')

    def on_new_task(self, task_id):
        """ New task event."""
        if self.node_worker_ref:
            self.node_worker_ref.get_task_and_add_to_queue(task_id)
            self.log.info(f'New task has been added task_id={task_id}')

        else:
            self.log.critical(
                'Task Master Node reference not set is socket namespace'
            )

    def on_container_failed(self, run_id):
        """A container in the collaboration has failed event.

        TODO handle run sequence at this node. Maybe terminate all
            containers with the same run_id?
        """
        self.log.critical(
            f"A container on a node within your collaboration part of "
            f"run_id={run_id} has exited with a non-zero status_code"
        )

    def on_expired_token(self, msg):
        self.log.warning("Your token is no longer valid... reconnecting")
        self.node_worker_ref.socketIO.disconnect()
        self.log.debug("Old socket connection terminated")
        self.node_worker_ref.server_io.refresh_token()
        self.log.debug("Token refreshed")
        self.node_worker_ref.connect_to_socket()
        self.log.debug("Connected to socket")
        self.node_worker_ref.sync_task_queue_with_server()
        self.log.debug("Tasks synced again with the server...")


# ------------------------------------------------------------------------------
class Node(object):
    """Node to handle incomming computation requests.

    The main steps this application follows: 1) retrieve (new) tasks
    from the central server, 2) kick-off docker algorithm containers
    based on this task and 3) retrieve the docker results and post
    them to the central server.

    TODO: read allowed repositories from the config file
    """

    def __init__(self, ctx):
        """ Initialize a new Node instance.

            Authenticates to the central server, setup encrpytion, a
            websocket connection, retrieving task that were posted while
            offline, preparing dataset for usage and finally setup a
            local proxy server.

            :param ctx: application context, see utils
        """
        self.log = logging.getLogger(logger_name(__name__))

        self.ctx = ctx
        self.config = ctx.config
        self.queue = queue.Queue()
        self._using_encryption = None

        # initialize Node connection to the server
        self.server_io = NodeClient(
            host=self.config.get('server_url'),
            port=self.config.get('port'),
            path=self.config.get('api_path')
        )

        self.log.info(f"Connecting server: {self.server_io.base_path}")

        # Authenticate with the server, obtaining a JSON Web Token.
        # Note that self.authenticate() blocks until it succeeds.
        self.log.debug("Authenticating")
        self.authenticate()

        # Setup encryption
        self.setup_encryption()

        # Thread for proxy server for algorithm containers, so they can
        # communicate with the central server.
        self.log.info("Setting up proxy server")
        t = Thread(target=self.__proxy_server_worker, daemon=True)
        t.start()

        # Create a long-lasting websocket connection.
        self.log.debug("Creating websocket connection with the server")
        self.connect_to_socket()

        # Check if new tasks were posted while offline.
        # self.log.debug("Fetching tasks that were posted while offline")
        # self.sync_task_queue_with_server()

        # If we're in a 'regular' context, we'll copy the dataset to our data
        # dir and mount it in any algorithm container that's run; bind mounts
        # on a folder will work just fine.
        #
        # If we're running in dockerized mode we *cannot* bind mount a folder,
        # because the folder is in the container and not in the host. We'll
        # have to use a docker volume instead. This means:
        #  1. we need to know the name of the volume so we can pass it along
        #  2. need to have this volume mounted so we can copy files to it.
        #
        #  Ad 1: We'll use a default name that can be overridden by an
        #        environment variable.
        #  Ad 2: We'll expect `ctx.data_dir` to point to the right place. This
        #        is OK, since ctx will be a DockerNodeContext.
        #
        #  This also means that the volume will have to be created & mounted
        #  *before* this node is started, so we won't do anything with it here.

        # We'll create a subfolder in the data_dir. We need this subfolder so
        # we can easily mount it in the algorithm containers; the root folder
        # may contain the private key, which which we don't want to share.
        # We'll only do this if we're running outside docker, otherwise we
        # would create '/data' on the data volume.
        if not ctx.running_in_docker:
            task_dir = ctx.data_dir / 'data'
            os.makedirs(task_dir, exist_ok=True)

        else:
            task_dir = ctx.data_dir

        self.log.debug("Setting up the docker manager")
        self.__docker = DockerManager(
            allowed_images=self.config.get("allowed_images"),
            tasks_dir=task_dir,
            isolated_network_name=f"{ctx.docker_network_name}-net",
            node_name=ctx.name,
            data_volume_name=ctx.docker_volume_name,
        )

        # login to the registries
        self.__docker.login_to_registries(
            self.ctx.config.get("docker_registries", [])
        )

        databases = {}

        # Check that the `default` database label is present. If this is
        # not the case, older algorithms will break
        db_labels = self.config['databases'].keys()
        if 'default' not in db_labels:
            self.log.error("'default' database not specified in the config!")
            self.log.debug(f'databases in config={db_labels}')

        # If we're running in a docker container, database_uri would point
        # to a path on the *host* (since it's been read from the config
        # file). That's no good here. Therefore, we expect the CLI to set
        # the environment variables for us. This has the added bonus that we
        # can override the URI from the command line as well.
        for label in db_labels:
            label_upper = label.upper()
            if self.__docker.running_in_docker():
                uri = os.environ[f'{label_upper}_DATABASE_URI']
            else:
                uri = self.config['databases'][label]

            db_is_file = Path(uri).exists()
            if db_is_file:
                # We'll copy the file to the folder `data` in our task_dir.
                self.log.info(f'Copying {uri} to {task_dir}')
                shutil.copy(uri, task_dir)

                # Since we've copied the database to the folder 'data' in the
                # root of the volume: '/data/<database.csv>'. We'll just keep
                # the basename (i.e. filename + ext).
                uri = os.path.basename(uri)

                self.__docker.database_is_file = True

            databases[label] = {'uri': uri, 'is_file': db_is_file}

        # Connect to the isolated algorithm network *only* if we're running in
        # a docker container.
        if ctx.running_in_docker:
            self.__docker.connect_to_isolated_network(
                ctx.docker_container_name,
                aliases=[cs.NODE_PROXY_SERVER_HOSTNAME]
            )

        # Let's keep it safe
        self.__docker.set_databases(databases)

        # Load additional environment vars for the algorithms. This is
        # for example usefull when a password is needed for the database
        self.__docker.algorithm_env = self.config.get('algorithm_env', {})

        # Thread for sending results to the server when they come available.
        self.log.debug("Start thread for sending messages (results)")
        t = Thread(target=self.__speaking_worker, daemon=True)
        t.start()

        # listen forever for incoming messages, tasks are stored in
        # the queue.
        self.log.debug("Starting thread for incoming messages (tasks)")
        t = Thread(target=self.__listening_worker, daemon=True)
        t.start()

        self.log.info('Init complete')

    def __proxy_server_worker(self):
        """ Proxy algorithm container communcation.

            A proxy for communication between algorithms and central
            server.
        """
        # supply the proxy server with a destination (the central server)
        # we might want to not use enviroment vars
        # os.environ["SERVER_URL"] = self.server_io.host
        # os.environ["SERVER_PORT"] = self.server_io.port
        # os.environ["SERVER_PATH"] = self.server_io.path

        if self.ctx.running_in_docker:
            # cs.NODE_PROXY_SERVER_HOSTNAME points to the name of the proxy
            # when running in the isolated docker network.
            default_proxy_host = cs.NODE_PROXY_SERVER_HOSTNAME
        else:
            # If we're running non-dockerized, assume that the proxy is
            # accessible from within the docker algorithm container on
            # host.docker.internal.
            default_proxy_host = 'host.docker.internal'

        # If PROXY_SERVER_HOST was set in the environment, it overrides our
        # value.
        proxy_host = os.environ.get("PROXY_SERVER_HOST", default_proxy_host)
        os.environ["PROXY_SERVER_HOST"] = proxy_host

        proxy_port = int(os.environ.get("PROXY_SERVER_PORT", 8080))

        # 'app' is defined in vantage6.node.proxy_server
        # app.debug = True
        proxy_server.app.config["SERVER_IO"] = self.server_io
        proxy_server.server_url = self.server_io.base_path

        for try_number in range(5):
            self.log.info(
                f"Starting proxyserver at '{proxy_host}:{proxy_port}'")
            http_server = WSGIServer(('0.0.0.0', proxy_port), proxy_server.app)

            try:
                http_server.serve_forever()

            except OSError as e:
                self.log.debug(f'Error during attempt {try_number}')
                self.log.debug(f'{type(e)}: {e}')

                if e.errno == 48:
                    proxy_port = random.randint(2048, 16384)
                    self.log.critical(
                        f"Retrying with a different port: {proxy_port}")
                    os.environ['PROXY_SERVER_PORT'] = str(proxy_port)

                else:
                    raise

            except Exception as e:
                self.log.error('Proxyserver could not be started or crashed!')
                self.log.error(e)

    def sync_task_queue_with_server(self):
        """ Get all unprocessed tasks from the server for this node."""
        assert self.server_io.cryptor, "Encrpytion has not been setup"

        # request open tasks from the server
        tasks = self.server_io.get_results(state="open", include_task=True)
        self.log.debug(tasks)
        for task in tasks:
            self.queue.put(task)

        self.log.info(f"received {self.queue._qsize()} tasks")

    def __start_task(self, taskresult):
        """Start a task.

            Start the docker image and notify the server that the task
            has been started.

            :param taskresult: an empty taskresult
        """
        task = taskresult['task']
        self.log.info("Starting task {id} - {name}".format(**task))

        # notify that we are processing this task
        self.server_io.set_task_start_time(taskresult["id"])

        token = self.server_io.request_token_for_container(
            task["id"],
            task["image"]
        )
        token = token["container_token"]

        # create a temporary volume for each run_id
        # FIXME: why is docker_temporary_volume_name() in ctx???
        vol_name = self.ctx.docker_temporary_volume_name(task["run_id"])
        self.__docker.create_volume(vol_name)

        # For some reason, if the key 'input' consists of JSON, it is
        # automatically marshalled? This causes trouble, so we'll serialize it
        # again.
        # FIXME: should probably find & fix the root cause?
        if type(taskresult['input']) == dict:
            taskresult['input'] = json.dumps(taskresult['input'])

        # Run the container. This adds the created container/task to the list
        # __docker.active_tasks
        local_db = task['database'] if task['database'] else 'default'
        self.__docker.run(
            result_id=taskresult["id"],
            image=task["image"],
            docker_input=taskresult['input'],
            tmp_vol_name=vol_name,
            token=token,
            database=local_db
        )

    def __listening_worker(self):
        """ Listen for incoming (websocket) messages from the server.

            Runs in a separate thread. Received events are dispatched
            through the appropriate action_handler for a channel.
        """
        self.log.debug("listening for incoming messages")

        # FIXME: while True in combination with a wait() call that never exits
        #   makes joining the tread (to terminate) difficult?
        while True:
            # incoming messages are handled by the action_handler instance
            # which is attached when the socket connection was made. wait()
            # is blocks forever (if no time is specified).
            try:
                self.socketIO.wait()
            except Exception as e:
                self.log.critical('Listening thread exception')
                self.log.debug(e)

    def __speaking_worker(self):
        """ Sending messages to central server.

            Routine that is in a seperate thread sending results
            to the server when they come available.

            TODO change to a single request, might need to reconsider
                the flow
        """
        self.log.debug("Waiting for results to send to the server")

        while True:
            try:
                results = self.__docker.get_result()

                # notify all of a crashed container
                if results.status_code:
                    self.socketIO.emit(
                        'container_failed',
                        data={
                            'node_id': self.server_io.whoami.id_,
                            'status_code': results.status_code,
                            'result_id': results.result_id,
                            'collaboration_id': self.server_io.collaboration_id
                        },
                        namespace='/tasks'
                    )

                self.log.info(
                    f"Sending result (id={results.result_id}) to the server!")

                # FIXME: why are we retrieving the result *again*? Shouldn't we
                # just store the task_id when retrieving the task the first
                # time?
                response = self.server_io.request(
                    f"result/{results.result_id}")
                task_id = response.get("task").get("id")

                if not task_id:
                    self.log.error(
                        f"task_id of result (id={results.result_id}) "
                        f"could not be retrieved"
                    )
                    return

                response = self.server_io.request(f"task/{task_id}")
                initiator_id = response.get("initiator")

                if not initiator_id:
                    self.log.error(
                        f"Initiator id from task (id={task_id})could not be "
                        f"retrieved"
                    )

                self.server_io.patch_results(
                    id=results.result_id,
                    initiator_id=initiator_id,
                    result={
                        'result': results.data,
                        'log': results.logs,
                        'finished_at': datetime.datetime.now().isoformat(),
                    }
                )
            except Exception as e:
                self.log.critical('Spreaker thread exception')
                self.log.debug(e)

    def authenticate(self):
        """ Authenticate to the central server

            Authenticate with the server using the api-key. If the
            server rejects for any reason we keep trying.
        """
        api_key = self.config.get("api_key")

        keep_trying = True
        i = 0
        while keep_trying and i < 10:
            i = i + 1
            try:
                self.server_io.authenticate(api_key)

            except Exception as e:
                msg = 'Authentication failed. Retrying in 10 seconds!'
                self.log.warning(msg)
                self.log.debug(e)
                time.sleep(10)

            else:
                # This is only executed if try-block executed without error.
                keep_trying = False

        # At this point, we shoud be connnected.
        self.log.info(f"Node name: {self.server_io.name}")

    def private_key_filename(self):
        """Get the path to the private key."""

        # FIXME: Code duplication: vantage6/cli/node.py uses a lot of the same
        #   logic. Suggest moving this to ctx.get_private_key()
        filename = self.config['encryption']["private_key"]

        # filename may be set to an empty string
        if not filename:
            filename = 'private_key.pem'

        # If we're running dockerized, the location may have been overridden
        filename = os.environ.get('PRIVATE_KEY', filename)

        # If ctx.get_data_file() receives an absolute path, its returned as-is
        fullpath = Path(self.ctx.get_data_file(filename))

        return fullpath

    def setup_encryption(self):
        """Setup encryption ... or don't."""
        encrypted_collaboration = self.server_io.is_encrypted_collaboration()
        encrypted_node = self.config['encryption']["enabled"]

        if encrypted_collaboration != encrypted_node:
            # You can't force it if it just ain't right, you know?
            raise Exception("Expectations on encryption don't match!?")

        if encrypted_collaboration:
            self.log.warn('Enabling encryption!')
            private_key_file = self.private_key_filename()
            self.server_io.setup_encryption(private_key_file)

        else:
            self.log.warn('Disabling encryption!')
            self.server_io.setup_encryption(None)

    def connect_to_socket(self):
        """ Create long-lasting websocket connection with the server.

            The connection is used to receive status updates, such as
            new tasks.
        """

        self.socketIO = SocketIO(request_timeout=60)

        self.socketIO.register_namespace(NodeTaskNamespace('/tasks'))
        NodeTaskNamespace.node_worker_ref = self

        self.socketIO.connect(
            url=f'{self.server_io.host}:{self.server_io.port}',
            headers=self.server_io.headers,
        )

        # Log the outcome
        while not self.socketIO.connected:
            self.log.debug('Waiting for socket connection...')
            time.sleep(1)

        self.log.info(f'Connected to host={self.server_io.host} on port='
                      f'{self.server_io.port}')

    def get_task_and_add_to_queue(self, task_id):
        """Fetches (open) task with task_id from the server.

            The `task_id` is delivered by the websocket-connection.
        """

        # fetch (open) result for the node with the task_id
        tasks = self.server_io.get_results(
            include_task=True,
            state='open',
            task_id=task_id
        )

        # in the current setup, only a single result for a single node
        # in a task exists.
        for task in tasks:
            self.queue.put(task)

    def run_forever(self):
        """Forever check self.queue for incoming tasks (and execute them)."""
        kill_listener = ContainerKillListener()
        try:
            while True:
                # blocking untill a task comes available
                # timeout specified, else Keyboard interupts are ignored
                self.log.info("Waiting for new tasks....")

                while not kill_listener.kill_now:
                    try:
                        task = self.queue.get(timeout=1)
                        # if no item is returned, the Empty exception is
                        # triggered, thus break statement is not reached
                        break

                    except queue.Empty:
                        pass

                    except Exception as e:
                        self.log.debug(e)

                if kill_listener.kill_now:
                    raise InterruptedError

                # if task comes available, attempt to execute it
                try:
                    self.__start_task(task)
                except Exception as e:
                    self.log.exception(e)

        except (KeyboardInterrupt, InterruptedError):
            self.log.info("Vnode is interrupted, shutting down...")
            self.socketIO.disconnect()
            sys.exit()


# ------------------------------------------------------------------------------
def run(ctx):
    """ Start the node."""
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("engineio.client").setLevel(logging.WARNING)


    # initialize node, connect to the server using websockets
    try:
        node = Node(ctx)
    except Exception as e:
        log = logging.getLogger(logger_name(__name__))
        log.critical(e)
        exit(1)

    # put the node to work, executing tasks that are in the que
    node.run_forever()
