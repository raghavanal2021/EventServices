"This is the Websocket Server for Algo Trading Frontend"

import tornado.websocket
import logging
import json
import os
import uuid

logging.basicConfig(filename="./logs/frontend_socket_server.log",level=os.getenv("loglevel"),filemode='w',
                    format='%(name)s:%(asctime)s - %(message)s')

class FrontEndSocket(tornado.websocket.WebSocketHandler):
    "Have the event websocket opened"
    clients = {}


    def check_origin(self, origin):
        "Pass any cross origin request"
        return True

    def open(self):
        "Called when the connection is established"
        logging.info("Connection Opened. Getting the metadata") 
        self.id = str(uuid.uuid4())

    def on_message(self,message):
        "Called when the client provides request to the server.Call the router"
        print(message)
        self.write_message(message)

    def on_close(self):
        "Called when the client disconnects"
        self.metadata.remove_disconnected_client(self.id)
        print("WebSocket Closed")
        


