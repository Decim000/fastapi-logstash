import logging

from logstash_async.handler import AsynchronousLogstashHandler

from settings import HOST_NAME, PORT, DATABASE_PATH


class Logger:
    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        self.logger.addHandler(AsynchronousLogstashHandler(
            HOST_NAME, PORT, database_path=DATABASE_PATH))
    
    async def info_on_get_request(self, message, uuid):
        self.logger.info(f'Got request from slave: {message}| UUID: {uuid}')

    async def info_on_send_request(self, message, uuid):
        self.logger.info(f'Send request to slave: {message}| UUID: {uuid}')