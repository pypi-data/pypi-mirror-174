import sys
import logging
import yaml
from os import path
from typing import Optional
from pydantic import BaseModel
from nt3core.logger import log


class ServiceConfig(BaseModel):
    port_grpc: Optional[int]
    timeout: int

    @staticmethod
    def from_dict(service_config: dict):
        """
    Deserializes a service configuration dictionary to a ServiceConfig object
        :param service_config: Service configuration dictionary
        :return: ServiceConfig object
        """
        try:
            service_config_detail = service_config.get("service_config", {})
            port_grpc = service_config_detail.get("port_grpc", -1)
            timeout = service_config_detail.get("timeout", 3)
            return ServiceConfig(port_grpc=port_grpc,
                                 timeout=timeout)
            pass
        except Exception as exception:
            raise Exception(f"Error deserializing service config dictionary: {exception}")

    @staticmethod
    def load_from_yaml_file(config_file: str, app: str):
        """
    Load a service configuration yaml file
        :param config_file: Filename of the config file
        :param app: Application calling this function, used for logging. Defaults to "Config Helper"
        :return: BaseConfig object
        """
        logger_app = logging.getLogger("application")
        if path.exists(config_file):
            with open(config_file, 'rt', encoding="utf-8") as file:
                try:
                    log.log_debug(logger=logger_app,
                                  app=app,
                                  message=f"Loading config file {config_file}")

                    config = yaml.safe_load(file.read())
                    log.log_debug(logger=logger_app, app=app, message=f"Service config file loaded - {config}")
                    return ServiceConfig.from_dict(config)
                except Exception as exception:
                    log.log_error(logger=logger_app,
                                  app=app,
                                  message=f"Error in reading service config file: {config_file}: {exception}")
                    return None
        else:
            log.log_error(logger=logger_app,
                          app=app,
                          message="Service config file not found or not provided")
            return None
