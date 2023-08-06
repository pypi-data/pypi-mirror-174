import os
from logging import getLogger

from .code import get_ga_client_id, check_tiledesk_api

logger = getLogger(__name__)

USERNAME = os.getenv("API_TILEDESK_USERNAME")
PASSWORD = os.getenv("API_TILEDESK_PASSWORD")

# check if the api key is set in the environment variables
if USERNAME is None:
    raise ValueError(
        "The USERNAME for TILEDESK is not set in the environment variables."
    )

# check if the api key is set in the environment variables
if PASSWORD is None:
    raise ValueError(
        "The PASSWORD key for TILEDESK is not set in the environment variables."
    )

if check_tiledesk_api(USERNAME, PASSWORD) is False:
    raise ValueError("The USERNAME or PASSWORD for TILEDESK is not valid.")
else:
    logger.info("The API for TILEDESK is working.")

if __name__ == "__main__":
    pass

