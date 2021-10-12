"Main class for Event Backbone"
import tornado
from eventsocket import EventSocket
from tornado.options import define, options
import logging
import pyfiglet
import os
from dotenv import load_dotenv

load_dotenv()
define("port", default=8888, help="run on the given port", type=int)
logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')

class EventBackBone(tornado.web.Application):
    "This class is the Event Backbone class"

    def __init__(self):
        ascii_banner = pyfiglet.figlet_format("Event Backbone")
        print("---------------------------------------------------------------------------------------------------------")
        print(ascii_banner)
        print("---------------------------------------------------------------------------------------------------------")
        logging.info(ascii_banner)
        handlers = [(r"/eventsocket",EventSocket)]
        super().__init__(handlers)
        logging.info("Event Backbone initialized")

def main():
    tornado.options.parse_command_line()
    app = EventBackBone()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()