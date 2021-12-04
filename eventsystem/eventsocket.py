"This is the Websocket Server for Algo Trading"

import tornado.websocket
import logging
import json
import os
import uuid
from metadata import ClientMetadata
from router import Router

logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',
                    format='%(name)s:%(asctime)s - %(message)s')

class EventSocket(tornado.websocket.WebSocketHandler):
    "Have the event websocket opened"
    clients = {}
    metadata =ClientMetadata()
    route= Router()

    def check_origin(self, origin):
        "Pass any cross origin request"
        return True

    def open(self):
        "Called when the connection is established"
        logging.info("Connection Opened. Getting the metadata") 
        self.id = str(uuid.uuid4())

    def get_list_connected_client(self):
        client_metadata = self.metadata.retrieve_clients()
        client_obj = json.loads(client_metadata)
        for client in client_obj:
            self.clients['client_id'] = client['client_id']
            self.clients['client_name'] = client['caller']
            self.clients['payload'] = client['payload']
            self.clients['track_id'] = client['track_id']
        print(f"{self.clients['client_id']} Connected {self.clients['client_name']}.Tracking ID is {self.clients['track_id']}")
        logging.info(f"{self.clients['client_id']} Connected {self.clients['client_name']}.Tracking ID is {self.clients['track_id']}")

    def on_message(self,message):
        "Called when the client provides request to the server.Call the router"
        print(message)
        return_code = self.route.routemessage(message=message,id=self.id)
        messagedetails = json.loads(message)
        if messagedetails['event_type'] != "keep_alive":
            self.get_list_connected_client()
        if return_code == -100:
            self.write_message(json.dumps({"event_type":"NACK","event_desc":"Error sending message to router. See logs"}))
        else:
            self.write_message(json.dumps({"event_type":"ACK","event_desc":"Message Sent to router"}))
            self.write_message(json.dumps(return_code))

    def on_close(self):
        "Called when the client disconnects"
        self.metadata.remove_disconnected_client(self.id)
        print("WebSocket Closed")
        


