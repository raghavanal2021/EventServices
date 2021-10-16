"This object routes the maps for the routes that we need to take"
import logging
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from models.responsemodel import ResponseModel
from handlers.metadata_handler import MetadataHandler
from handlers.keepalive_handler import KeepAliveHandler
from handlers.handler_factory import HandlerFactory

load_dotenv()
logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class MapRouter():
    "A maprouter object that returns the contract for the destination function"

    def __init__(self):
        "Initialize the router"
        logging.info(f"Getting routes from the file {os.getenv('router')}")
        self.routes =json.loads(os.getenv("router"))
        self.metadata_handler = MetadataHandler()
        self.keepalive_handler = KeepAliveHandler()
        self.handler_factory = HandlerFactory()
        self.response_model = ResponseModel()

    def get_destination_contract(self,contract,id):
        "Parse the incoming message and find the next destination based on the route map"
        contract_obj = json.loads(json.dumps(contract))
        print(contract_obj)
        requesttype = contract_obj['event_type']
        client_id = contract_obj['client_id']
        track_id = id
        try:
                "Call the Keep Alive Handler to handle the keep Aliver Method"
                if requesttype == "keep_alive":
                    keep_alive_response= self.keepalive_handler.route_keep_alive(client_id)
                    return keep_alive_response
                "Route to Metadata Handler if the request type is to insert the client information"
                if requesttype == "metadata":
                    metadata_response = self.metadata_handler.insert_new_client(caller=contract_obj['event_producer'],
                                                                                client_id=contract_obj['client_id'],
                                                                                payload=contract_obj['payload'],
                                                                                track_id=track_id)
                    return metadata_response                
                "Route all other handlers to the appropriate factory objects"
                if requesttype != "keep_alive" and requesttype != "metadata":
                    logging.info(f"Calling Factory for the event {requesttype}")
                    handler_response = self.handler_factory.get_handler(requesttype,contract)                    
                    return handler_response
        except Exception as e:
                logging.error(f"Error in routing. Exception : {e}")
                return json.dumps({"statuscode":-100,"error":e})

    def get_response_json(self,requesttype,payload, client_id,track_id):
        "Map the destination and get the response json"
        desttype = list(self.routes[requesttype])
        response_object = None
        print(desttype)
        data = json.loads(payload)
        for destination in desttype:
            logging.info(f"Preparing Contract for the destination {destination}")
            logging.info(f"Contract is {payload[destination]}")
            self.response_model.event_type = destination
            self.response_model.event_ts = str(datetime.now().isoformat())
            self.response_model.get_client_id = client_id
            self.response_model.get_track_id = track_id
            self.response_model.get_payload = payload[destination]
            output_dict = {"event_type":self.response_model.event_type,"event_ts":self.response_model.event_ts,
                            "client_id":self.response_model.client_id,"track_id":self.response_model.track_id,"payload":self.response_model.payload}
            return json.dumps(output_dict)
