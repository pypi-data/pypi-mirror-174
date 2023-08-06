import re
import subprocess as sp
from signal import SIGINT
from threading import Thread

from .common import cyan_print


class Factory:
    """This class encapsulates a process that manages the python provider factory dotnet application

    """

    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            domain: str,
            _fbn_run: bool,
    ):
        """Constructor of the Factory class

        Args:
            host (str): the host that the target api server is running at
            port (int): the port that the target api server is exposed at
            user (str): the user to route with. Can be a user ID, global or None. In the none case a browser window will
             be opened for you to log in with.
            domain (str): which finbourne domain to run in such as fbn-ci (internal), fbn-qa (internal) or fbn-prd.
            _fbn_run (bool): finbourne-internal option for an alternative rabbitMQ authentication when running in K8s.

        """

        if re.match('^[\w._-]+$', host) is None:
            raise ValueError(f"Invalid value for host: {host}")

        if not isinstance(port, int):
            raise ValueError(f"Port number must be an integer. Was {type(port).__name__} ({port})")

        self.cmd = f'luminesce-python-providers --quiet --authClientDomain={domain} '

        if user is not None and user != 'global':
            self.cmd += f'--localRoutingUserId "{user}" '

        elif user is not None and user == 'global':
            self.cmd += f'--routeAs:Global '

        self.cmd += f'--config "PythonProvider:BaseUrl=>http://{host}:{port}/api/v1/" '
        if _fbn_run:
            self.cmd += '"NameServiceClient:RabbitConfigFile=>honeycomb-rabbit-config-plain.json" '
            self.cmd += '"NameServiceClient:RabbitUserPassword->/usr/app/secrets/service-main" '

        self.block = True
        self.process = None
        self.monitor_thread = Thread(target=self.__monitor)

    def start(self):
        """Start the factory process. This will block the program while the setup is running.

        """
        cyan_print('Starting python provider factory')
        print(self.cmd, end='\n\n')

        self.process = sp.Popen(self.cmd.split(), shell=False, stdout=sp.PIPE, stderr=sp.PIPE)

        self.monitor_thread.start()

        while self.block:
            pass

    def stop(self):
        """Stop the factory process and shut down the providers. This will block the program while the termination is
        completing.

        """

        self.block = True

        cyan_print('\nStopping python provider factory')

        self.process.send_signal(SIGINT)

        while self.block:
            pass

        self.monitor_thread.join()

    def __monitor(self):

        # Set a loop running in another thread that periodically polls the process
        # When there's a new line of output print it
        # If the process is in exit state, set block=False so the stop method stops blocking
        while True:

            output = self.process.stdout.readline().decode('utf-8').rstrip()

            if output:
                print(output)

            if 'Running! Hit Ctrl+C to shut down services' in output:
                self.block = False

            if self.process.poll() is not None:
                break

        self.block = False
