"This is the event router that will route messages to the correct services"

import logging
import os
import json
from dotenv import load_dotenv
from routemapper import MapRouter
logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
load_dotenv()
class Router():
    "This class will be instantiated once and will route the messages to the particular service"

    def __init__(self):
        "Initialize the class"
        logging.info("Router class initialized")
        self.map_object = MapRouter()

    def routemessage(self,message,id):
        "Route the message to the appropriate publisher. JSON contract is {type:requesttype, caller:callerid, payload}"
        json_message = message
        print(f"Routing Message --> {message} ")
        msg_object = json.loads(json_message)    
        # if msg_object['event_type'] != "keep_alive":
        dest_contract = self.map_object.get_destination_contract(msg_object,id)
        return dest_contract
        #else:
        #    return json_message
