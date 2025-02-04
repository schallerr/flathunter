"""Functions and classes related to sending Telegram messages"""
import json
import requests

from flathunter.logging import logger
from flathunter.abstract_processor import Processor

class SenderMattermost(Processor):
    """Expose processor that sends Mattermost messages"""

    def __init__(self, config):
        self.config = config
        self.webhook_url = self.config.get('mattermost', {}).get(
            'webhook_url', '')

    def process_expose(self, expose):
        """Send a message to a user describing the expose"""
        message = self.config.get('message', "").format(
            title=expose['title'],
            rooms=expose['rooms'],
            size=expose['size'],
            price=expose['price'],
            url=expose['url'],
            address=expose['address'],
            durations="" if 'durations' not in expose else expose[
                'durations']).strip()
        self.send_msg(message)
        return expose

    def send_msg(self, message):
        """Send messages to the mattermost webhook"""
        logger.debug(('webhook_url:', self.webhook_url))
        logger.debug(('message', message))
        resp = requests.post(
            self.webhook_url,
            data=json.dumps({"text": message})
        )
        logger.debug("Got response (%i): %s", resp.status_code,
                           resp.content)
        # handle error
        if resp.status_code != 200:
            logger.error(
                "When sending mattermost bot message, we got status %i with message: %s",
                resp.status_code,
                resp.text
            )
