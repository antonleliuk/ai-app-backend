import logging

class UnknownMessageHandler:
    @staticmethod
    def handler_code():
        return "unknown"
    
    # pylint: disable-next=unused-argument
    def handle(self, message = None):
        logging.warning("Unknown handler doesn't know how to handle message")