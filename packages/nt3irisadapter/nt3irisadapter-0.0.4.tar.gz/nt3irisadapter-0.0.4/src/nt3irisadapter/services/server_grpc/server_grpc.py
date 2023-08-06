import logging
import uuid
from concurrent import futures
import grpc
from src.nt3irisadapter.services.model import pos_service_pb2_grpc as pos_grpc
from src.nt3irisadapter.services.model.service_config import ServiceConfig
from src.nt3irisadapter.services.model.pos_service_pb2 import Status, CheckServiceResponse, StatusType
from nt3core.logger import log
from nt3core.logger.log_context import ctx
from src.nt3irisadapter.services.logic.iris_adapter import IRISAdapter


# noinspection PyUnresolvedReferences,PyBroadException
class Listener(pos_grpc.POSServicer):

    def __init__(self, service_config: ServiceConfig) -> None:
        """
    Initialize the grpc listener
        :param service_config: ServiceConfig object containing the service specific settings
        """
        # initialize logger
        self._logger_app = logging.getLogger("application")
        self._logger_comm = logging.getLogger("communication")

        # store configs
        self._api_name = "IRIS Adapter"
        self._service_config = service_config
        try:
            log.log_debug(self._logger_app, self._api_name, f"Initializing IRIS Adapter grpc server")

            # create POS service logic class
            self._iris_adapter = IRISAdapter(service_config=service_config)

            super().__init__()
        except Exception as exception:
            log.log_error(self._logger_app, self._api_name,
                          f"Error initializing the IRIS Adapter grpc listener: {exception}")

    # region Methods from requests

    def CheckService(self, request, context):
        """
    Checks if the IRIS Adapter service is running, triggered by the grpc server
        :param request: sent by the grpc server
        :param context: sent by the grpc server
        """
        # generate trace id for request
        ctx.trace_id = str(uuid.uuid4())

        try:
            # log request message
            log.log_debug(self._logger_comm, self._api_name, "CheckService|IN|Request received", trace_id=True)

            response = self._iris_adapter.check_service()

            # log response message
            log.log_debug(self._logger_comm, self._api_name, f"CheckPartner|OUT|\n{response}", trace_id=True)
            return response
        except Exception as exception:
            log.log_error(self._logger_comm, self._api_name, f"Error: {exception}", trace_id=True)
            return _get_error_object(CheckServiceResponse, str(exception))

    # endregion


class Server:

    def __init__(self, service_config: ServiceConfig) -> None:
        """
    Initialize grpc server
        :param service_config: ServiceConfig object containing the service specific settings
        """
        # initialize logger
        self._logger_app = logging.getLogger("application")
        self._logger_comm = logging.getLogger("communication")

        # store configs
        self._service_config = service_config
        self._api_name = "IRIS Adapter"
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    def serve(self):
        """
    Starts the grpc server
        """
        try:
            pos_grpc.add_POSServicer_to_server(
                Listener(service_config=self._service_config),
                self.server)
            log.log_info(self._logger_app, self._api_name,
                         f"Starting grpc server for IRIS Adapter on port {self._service_config.port_grpc}")
            self.server.add_insecure_port(f"[::]:{self._service_config.port_grpc}")
            self.server.start()
            while True:
                pass
        except Exception as exception:
            raise exception

    def stop(self):
        """
    Stops the server
        """
        self.server.stop(0)


# noinspection PyCallingNonCallable
def _get_error_object(response_object: object, message: str) -> object:
    """
Generates an error object
    :param response_object: Response object used for the error response
    :param message: Status message
    :return: Error response object
    """
    status = Status(
        type=StatusType.ERROR,
        message=str(message)
    )
    response = response_object(status=status)
    return response
