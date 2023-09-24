import io
import base64
import logging
import openai

from PIL import Image

from variables import variables
from waveshare_epd_driver import epd5in83 as epd_driver

# TODO temporary, change to INFO
epd_driver.logger.setLevel(logging.DEBUG)

openai.api_key = variables.openai_api_key()

class DrawMessageHandler():
    def __init__(self) -> None:
        self.epd = epd_driver.EPD()
    @staticmethod
    def handler_code():
        return "draw"
    
    def handle(self, message):
        image = self._generate_image_from_text(message)
        # TODO publish message back with results to say draw or not
        if image is not None:
            image.save("test.png")
            self._print_image(image)

    def _generate_image_from_text(self, message) -> Image:
        prompt = message["text"]
        # print generating placeholder
        logging.info("Geneating image for prompt: %s", prompt)
        try:
            response = openai.Image.create(prompt = prompt, n = 1, size = "512x512", response_format = "b64_json")
            logging.info("Create image for prompt: %s", prompt)
            images = response["data"]
            if images:
                image_bytes = base64.b64decode(images[0]["b64_json"])
                return Image.open(io.BytesIO(image_bytes))
                
        except BaseException:
            logging.error("Error during image creation", exc_info=True)
        return None
    
    def _print_image(self, image: Image):
        logging.info("Start drawing image")
        status = self.epd.init()
        logging.info("Initialized status: %s. Clearing display", status)
        self.epd.Clear()
        # Convert the image to 1-bit mode
        # "600x448"
        eink_image = image.resize(size = (600, 448)).convert("1")
        # eink_image = image.convert("1")
        eink_image.save("test_1.bmp")
        logging.info("Image converted to e-ink")
        # display image
        self.epd.display(self.epd.getbuffer(eink_image))
        logging.info("Image displayed. Sleeping...")
        self.epd.sleep()