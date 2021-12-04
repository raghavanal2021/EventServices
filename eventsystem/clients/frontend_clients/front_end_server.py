"Main class for Front End Server"
import tornado
from frontend_socket_server import FrontEndSocket
from tornado.options import define, options
import logging
import pyfiglet
import os
from dotenv import load_dotenv

load_dotenv()
define("port", default=9300, help="run on the given port", type=int)
logging.basicConfig(filename="./logs/frontend_clients.log",level=os.getenv("loglevel"),filemode='w',format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')

class FrontEndSocketServer(tornado.web.Application):
    "This class is the Event Backbone class"

    def __init__(self):
        ascii_banner = pyfiglet.figlet_format("Front End Server")
        print("---------------------------------------------------------------------------------------------------------")
        print(ascii_banner)
        print("---------------------------------------------------------------------------------------------------------")
        logging.info(ascii_banner)
        handlers = [(r"/frontend_socket_server",FrontEndSocket)]
        super().__init__(handlers)
        logging.info("Front End Socket Server initialized")

def main():
    tornado.options.parse_command_line()
    app = FrontEndSocketServer()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()