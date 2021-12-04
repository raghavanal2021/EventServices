"This will handle all the Metadata request and provide the response to the routers "

import logging
import os
from models.responsemodel import ResponseModel
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import json

logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',format='%(levelname)s : %(filename)s -%(asctime)s - %(message)s')
load_dotenv()
class MetadataHandler():

    def __init__(self):
        logging.info("Metadata Request is running...")
        "Initializes the Database credentials."
        mongo_host = os.getenv("mongohost")
        mongo_port = int(os.getenv("mongoport"))
        connection = MongoClient(mongo_host,mongo_port)
        database = connection['EventSystem']
        self.collection = database['Clientinformation']
        self.response = ResponseModel()

    def insert_new_client(self,caller,client_id,payload,track_id):
        "Insert the metadata for the new clients"
        json_object = {"caller":caller,"client_id":client_id,"payload":payload,"track_id":track_id}
        try:
            self.collection.insert_one(json_object)
            logging.info("Loaded the Client information to Database..")
            self.response.client_id = client_id
            self.response.event_ts = str(datetime.now().isoformat())
            self.response.event_type = 'ACK'
            self.response.payload = {"ackmessage":"Client Registered successfully...","status":100}
            self.contract = {"event_type":self.response.event_type,"event_ts":self.response.event_ts,
                                "client_id":self.response.client_id,"payload":self.response.payload}
            return json.dumps(self.contract)
        except Exception as e:
            self.response.client_id = client_id
            self.response.event_ts = str(datetime.now().isoformat())
            self.response.event_type = 'NACK'
            self.response.payload = {"ackmessage":e,"status":-100}
            self.contract = {"event_type":self.response.event_type,"event_ts":self.response.event_ts,
                                "client_id":self.response.client_id,"payload":self.response.payload}
            logging.error(f"Error uploading the metadata to the database {e}")
            return json.dumps(self.contract)

    def retrieve_clients(self):
        "Retrieve the clients from the database"
        try:
            cur = self.collection.find({},{"_id":0})
            output = list(cur)
            return json.dumps(output)
        except Exception as e:
            logging.error(f"Error while retrieving the clients {e}")

    def remove_disconnected_client(self,client_id):
        "Remove a disconnected client"
        try:
            self.collection.delete_one({"track_id":client_id})
            logging.info(f"Deleted the disconnected client {client_id}")
        except Exception as e:
            logging.error(f"Error removing disconnected client {e}")