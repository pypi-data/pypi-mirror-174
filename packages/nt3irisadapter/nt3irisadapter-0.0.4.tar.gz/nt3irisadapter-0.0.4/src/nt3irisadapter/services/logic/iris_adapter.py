import logging

from nt3core.logger import log
from src.nt3irisadapter.services.model.service_config import ServiceConfig
from src.nt3irisadapter.services.model.pos_service_pb2 import Status, CheckServiceResponse, StatusType


class IRISAdapter:
    def __init__(self, service_config: ServiceConfig):

        # initialize logger
        self._logger_app = logging.getLogger("application")
        self._logger_comm = logging.getLogger("communication")

        # store configs
        self._service_config = service_config

    def check_service(self) -> CheckServiceResponse:
        """
    Check if service is running
        :return: CheckServiceResponse
        """
        try:
            # create CheckServiceResponse object
            status = Status(
                type=StatusType.OK,
                message="Service up and running"
            )
            response = CheckServiceResponse(
                status=status
            )
            return response
        except Exception as exception:
            log.log_error(self._logger_comm, self._api_name, f"Error: {exception}", trace_id=True)
            return _get_error_object(CheckServiceResponse, str(exception))

    # region Helpers


# noinspection PyCallingNonCallable
def _get_error_object(response_object: object, message: str) -> str:
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
    return response

    # endregion
