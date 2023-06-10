import logging
from dotenv import dotenv_values

from pydantic import BaseSettings

logger = logging.getLogger('hubspot_clickup_syncer')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

# Info logger creaton

info_logger = logging.FileHandler('logs/info.log', mode='a')
info_logger.setLevel(logging.DEBUG)
info_logger.setFormatter(formatter)

# Error logger creation

error_logger = logging.FileHandler('logs/error.log', mode='a')
error_logger.setLevel(logging.ERROR)
error_logger.setFormatter(formatter)

logger.addHandler(info_logger)
logger.addHandler(error_logger)

class Settings(BaseSettings):
    # Settings objects getting values from .env file to set environment variables
    config = dotenv_values(".env")

    hubspot_access_token = config["HUBSPOT_ACCESS_TOKEN"]
    clickup_access_token = config["CLICKUP_ACCESS_TOKEN"]
    clickup_list_id = config["CLICKUP_LIST_ID"]
    database_url = config["DATABASE_URL"]