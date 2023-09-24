import os
from typing import Any
from dotenv import load_dotenv

class VariablesMeta(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]

class Variables(metaclass=VariablesMeta):
    def __init__(self) -> None:
        pass

    def load(self) -> None:
        load_dotenv()

    def openai_api_key(self):
        return os.getenv("OPENAI_API_KEY")

    def mq_host(self):
        return os.getenv("MQ_HOST")
    
variables = Variables()