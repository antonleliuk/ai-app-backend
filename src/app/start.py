import logging
import sys

# import variables # this should be first to load variables

from variables import variables
from mq import MessageListener

if __name__ == '__main__':
    variables.load()
    logging.basicConfig(level=logging.INFO)

    listener = None
    try:
        logging.info("start")
        
        listener = MessageListener()
        listener.start()
        logging.info('working...')
        while True:
            pass
    except KeyboardInterrupt:
        print("\nCtrl+C detected in the main thread. Stopping worker thread...")
        if listener is not None:
            listener.stop()
        sys.exit(0)