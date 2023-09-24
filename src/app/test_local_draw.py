import logging

from PIL import Image
from variables import variables
from handlers.draw.draw_handler import DrawMessageHandler

logging.basicConfig(level=logging.INFO)
variables.load()

handler = DrawMessageHandler()

with Image.open("test.png") as image:
    handler._print_image(image)