"This will capture the client's metadata and will retrieve client information from cache"

import logging
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json

load_dotenv()
logging.basicConfig(filename="./logs/eventbackbone.log",level=logging.INFO,filemode='w',format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class ClientMetadata():
    "The metadata object will connect to the Mongo Database and inserts and retrieves client information"

    def __init__(self):
        "Initializes the Database credentials."
        mongo_host = os.getenv("mongohost")
        mongo_port = int(os.getenv("mongoport"))
        connection = MongoClient(mongo_host,mongo_port)
        database = connection['EventSystem']
        self.collection = database['Clientinformation']

    def insert_new_client(self,caller,client_id,payload,track_id):
        "Insert the metadata for the new clients"
        json_object = {"caller":caller,"client_id":client_id,"payload":payload,"track_id":track_id}
        try:
            self.collection.insert_one(json_object)
            logging.info("Loaded the Client information to Database..")
            return json.dumps({"requesttype":"metadataupdate","status":100})
        except Exception as e:
            logging.error(f"Error uploading the metadata to the database {e}")
            return json.dumps({"requesttype":"metadataupdate","status":-100})

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


