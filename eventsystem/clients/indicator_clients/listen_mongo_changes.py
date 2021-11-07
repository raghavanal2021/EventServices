"Listen to Mongo Database Changes"
import logging, os
import json, pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from run_indicator_list import RunIndicator
import pandas as pd


load_dotenv()
class Listen_Changes():

    def __init__(self,strategy_id,indicator_list):
        _host = os.getenv("mongohost")
        _port = int(os.getenv("mongoport"))
        self._client = MongoClient(_host,_port)
        self._db = self._client["ChangeDB"]
        self._runind = RunIndicator(strategy_id=strategy_id,indicator_list=indicator_list)
        #self.dataframe = pd.DataFrame(columns=['timestamp','open','high','low','close','volume','ticker'],index=['timestamp'])

    def watchchanges(self,strategy_id:str,indicator_list):
        self.coll = self._db[str(strategy_id)]
        outputcursor = self.coll.find({},{"_id":0})
        df = pd.DataFrame(list(outputcursor))
        while True:
            change_stream = self._db[str(strategy_id)].watch()
            document = next(change_stream)
            df = df.append(document['fullDocument'],ignore_index=True)
            self._runind.next(df)
            