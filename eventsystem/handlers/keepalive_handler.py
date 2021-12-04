"This will handle all keep alive handlers and provide a response to the router"

import logging
import os
from models.responsemodel import ResponseModel
from datetime import datetime


logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',format='%(levelname)s : %(filename)s -%(asctime)s - %(message)s')
class KeepAliveHandler():
    "This class will handle all keep alive events generated from the clients"

    def __init__(self):
        logging.info("Keep Alive Handler running")

    def route_keep_alive(self,client_id):
        logging.info(f"{client_id} sent a keep alive signal")
        self.client_id = client_id
        response_contract = self.create_response_object()
        return response_contract

    def create_response_object(self):
        response = ResponseModel()
        response.event_type = 'ACK'
        response.event_ts = str(datetime.now().isoformat())
        response.client_id = self.client_id
        response.payload = {"client_id": self.client_id,"event_type":"keepalive" }
        contract = {"event_type":response.event_type, "event_ts":response.event_ts,"client_id":response.client_id,"payload":response.payload}
        logging.info(f"Contract {contract}")
        return contract
