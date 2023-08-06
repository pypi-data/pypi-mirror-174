import os
import logging
from distutils.util import strtobool

from dotenv import dotenv_values

logging.basicConfig(
    level=os.getenv("LQS_LOG_LEVEL") or logging.INFO,
    format="%(asctime)s  (%(levelname)s - %(name)s): %(message)s",
)
logger = logging.getLogger(__name__)

from .interface import Lister, Getter, Creator, Updater, Deleter, S3


class LogQS:
    def __init__(self, api_url=None, api_key_id=None, api_key_secret=None, pretty=None):
        self._env_config = {**dotenv_values(".env"), **os.environ}

        self._api_url = api_url if api_url else self._env_config.get("LQS_API_URL")
        if not self._api_url:
            raise ValueError("No API URL provided")
        self._api_key_id = (
            api_key_id if api_key_id else self._env_config.get("LQS_API_KEY_ID")
        )
        if not self._api_key_id:
            raise ValueError("No API Key ID provided")
        self._api_key_secret = (
            api_key_secret
            if api_key_secret
            else self._env_config.get("LQS_API_KEY_SECRET")
        )
        if not self._api_key_secret:
            raise ValueError("No API Key Secret provided")

        self._pretty = (
            pretty
            if pretty
            else bool(strtobool(self._env_config.get("LQS_PRETTY", "false")))
        )

        self.config = {
            "api_url": self._api_url,
            "api_key_id": self._api_key_id,
            "api_key_secret": self._api_key_secret,
            "pretty": self._pretty,
        }

        logger.debug("config: %s", self.config)

        self.list = Lister(config=self.config)
        self.get = Getter(config=self.config)
        self.create = Creator(config=self.config)
        self.update = Updater(config=self.config)
        self.delete = Deleter(config=self.config)

        self.s3 = S3(creator=self.create)
