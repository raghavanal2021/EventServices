"Insert the payload into Mongo Database"

from pymongo import MongoClient
import logging, os,json
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename="../indicator_clients/logs/indicator_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class InsertPayload():
    "This class inserts the payload into Mongo database for tracking changes"
    def __init__(self):
        _host = os.getenv("mongohost")
        _port = int(os.getenv("mongoport"))
        self._client = MongoClient(_host,_port)

    def insert_data(self,contract,strategy_id,db):
        try:
            self._db = self._client[db]
            self._coll = self._db[str(strategy_id)]
            contract_obj = json.loads(contract)
            self._coll.update(contract_obj,contract_obj,upsert=True)
        except Exception as e:
            logging.error(f"Exception while loading the data into Database --> {e}")
        return None