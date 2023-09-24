from .draw.draw_handler import DrawMessageHandler
from .unknown import UnknownMessageHandler

class MessageHandlerFactory:
    def __init__(self) -> None:
        self.handlers = {
            DrawMessageHandler.handler_code(): DrawMessageHandler()
        }

    def resolve_handler(self, code):
        return self.handlers.get(code, UnknownMessageHandler())
    
factory = MessageHandlerFactory()