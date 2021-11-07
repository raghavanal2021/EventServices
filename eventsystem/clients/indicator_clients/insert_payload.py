"Insert the payload into Mongo Database"

from pymongo import MongoClient
import logging, os,json
from dotenv import load_dotenv

load_dotenv()
class InsertPayload():
    "This class inserts the payload into Mongo database for tracking changes"
    def __init__(self):
        _host = os.getenv("mongohost")
        _port = int(os.getenv("mongoport"))
        self._client = MongoClient(_host,_port)
        self._db = self._client["ChangeDB"]

    def insert_data(self,contract,strategy_id):
        self._coll = self._db[str(strategy_id)]
        contract_obj = json.loads(contract)
        self._coll.update(contract_obj,contract_obj,upsert=True)
        return None