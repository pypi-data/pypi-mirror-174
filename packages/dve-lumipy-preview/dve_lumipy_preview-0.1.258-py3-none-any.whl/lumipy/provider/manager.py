import time
from typing import Optional

from .api_server import ApiServer
from .base_provider import BaseProvider
from .factory import Factory
from .common import red_print, cyan_print
from lumipy.common.string_utils import indent_str
import re
import traceback


class ProviderManager:
    """Class that manages the configuration and running of python-based Luminesce providers.

    """

    def __init__(
            self,
            *providers: BaseProvider,
            host: Optional[str] = '127.0.0.1',
            port: Optional[int] = 5001,
            dry_run: Optional[bool] = False,
            user: Optional[str] = None,
            domain: Optional[str] = 'fbn-prd',
            _fbn_run: Optional[bool] = False
    ):
        """Constructor of the ProviderManager class.

        Args:
            *providers (BaseProvider): local provider instances (classes that inherit from BaseProvider) that
            the server should manage.
            host (Optional[str]): optional server host path. Defaults to localhost.
            port (Optional[int]): optional port for the server to use. Defaults to 5000.
            dry_run (Optional[bool]): whether to only run the web server and not start the local provider factory.
            user (Optional[str]): optional user id, or 'global' to run the providers for. You can also specify 'global'
            to run the provider globally.
            domain (Optional[str]): lusid environment to run in. Defaults to fbn-prd.
            _fbn_run (Optional[bool]): Finbourne-internal. Alternative way to authenticate with RabbitMQ when running in
            Finbourne's k8s clusters.

        """
        if len(providers) == 0:
            raise ValueError(
                "Nothing to run! No providers have been supplied to the provider server constructor"
            )

        if re.match('^[\w._-]+$', host) is None:
            raise ValueError(f"Invalid value for host: {host}")

        if not isinstance(port, int):
            raise ValueError(f"Port number must be an integer. Was {type(port).__name__} ({port})")

        if user is not None and not user.isalnum():
            raise ValueError(f"Invalid user ID ({user}), must be alphanumeric characters only. ")

        if re.match('^[\w_-]+$', domain) is None:
            raise ValueError(f"Invalid value for domain: {domain}")

        self.dry_run = dry_run
        self.api_server = ApiServer(*providers, host=host, port=port)
        self.factory = Factory(host, port, user, domain, _fbn_run)

    def __start(self):
        cyan_print(f'Launching providers! 🚀')
        self.api_server.start()
        if not self.dry_run:
            self.factory.start()
        else:
            red_print('⚠️  dry_run=True: only running provider APIs.')
        cyan_print('\n🟢 Providers are ready to use.')
        cyan_print('Use ctrl+c or the stop button in jupyter to shut down\n')

    def __stop(self, exc_type, exc_val, exc_tb):

        if exc_type == KeyboardInterrupt:
            red_print("\n⚠️  Received keyboard interrupt.")

        elif exc_type is not None:
            red_print(f"\n💥 An unexpected {exc_type.__name__} occurred: \"{exc_val}\"")
            red_print("  Traceback (most recent call last):")
            red_print(indent_str(''.join(traceback.format_tb(exc_tb))))
            red_print("  Trying to shut down before rethrow...")

        cyan_print('\n🟡 Providers are shutting down.')
        if not self.dry_run:
            self.factory.stop()
        self.api_server.stop()
        cyan_print(f'\n🔴 Providers are shut down.\n')

    def __enter__(self):
        self.__start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__stop(exc_type, exc_val, exc_tb)

    def run(self):
        """Run the manager instance in the foreground. The manager can be shut down with a KeyboardInterupt (ctrl+C).

        """
        self.__start()
        while True:
            try:
                # block
                time.sleep(5)
            except KeyboardInterrupt as ke:
                self.__stop(type(ke), None, None)
                raise ke
            except Exception as e:
                self.__stop(type(e), str(e), e.__traceback__)
                raise e
