"Indicator Response Handler"

import os,logging,json
from dotenv import load_dotenv
from pymongo import MongoClient
logging.basicConfig(filename="../indicator_clients/logs/indicator_response.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
load_dotenv()
class ResponseHandler():
    "This class listens to the Mongodb changs in indicator and sends the response to the event backbone for further processing"
    def __init__(self):
        _host = os.getenv("mongohost")
        _port = int(os.getenv("mongoport"))
        try:
            self._mclient = MongoClient(_host,_port)
            self._db = self._mclient["Indicators"]
            logging.info("Response Watch Initiated")
        except Exception as e:
            print(e)
            logging.error(f"Exception in listening for response --> {e} ")

    def watchchanges(self):
            try:
                change_stream = self._db.watch()
                document = next(change_stream)
                contract_obj = document['fullDocument']
                contract_obj.pop("_id")
                print(f"Response to Event Backbone --> {contract_obj}")
            except Exception as e:
                logging.error(f"Exception in listening changes --> {e}")
            return contract_obj