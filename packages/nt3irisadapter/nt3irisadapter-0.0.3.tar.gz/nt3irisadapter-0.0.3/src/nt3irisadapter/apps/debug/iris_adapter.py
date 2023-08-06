from nt3core.logger import logger_config
from src.nt3irisadapter.services.model.service_config import ServiceConfig
from src.nt3irisadapter.services.server_grpc.server_grpc import Server

if __name__ == "__main__":
    # load configuration files
    logger_config.setup_logger(
        "/config/debug/iris_adapter_log.yaml")
    service_config = ServiceConfig.load_from_yaml_file(
        "/config/debug/iris_adapter_config.yaml",
        "IRIS Adapter")

    # if rest port is set, start rest server
    if service_config.port_grpc != -1:
        server = Server(service_config=service_config)
        server.serve()
