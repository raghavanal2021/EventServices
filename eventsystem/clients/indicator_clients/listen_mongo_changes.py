"Listen to Mongo Database Changes"
from datetime import datetime
import logging, os
import json, pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from run_indicator_list import RunIndicator
import pandas as pd
from model.responsemodel import ResponseModel
from insert_payload import InsertPayload

load_dotenv()
logging.basicConfig(filename="../indicator_clients/logs/indicator_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class Listen_Changes():

    def __init__(self,strategy_id,indicator_list,client_id):
        _host = os.getenv("mongohost")
        _port = int(os.getenv("mongoport"))
        try:
            self._client_id = client_id
            self._client = MongoClient(_host,_port)
            self._db = self._client["ChangeDB"]
            self._runind = RunIndicator(strategy_id=strategy_id,indicator_list=indicator_list)
            self.payload_contract = InsertPayload()
            logging.info("Started to route the message request to the message handler")
            #self.output_listener = Indicator_Listener("ws://localhost:8888/eventsocket",5)
        except Exception as e:
            logging.error(f"Exception in listening for changes --> {e} ")
        
        #self.dataframe = pd.DataFrame(columns=['timestamp','open','high','low','close','volume','ticker'],index=['timestamp'])

    def watchchanges(self,strategy_id,indicator_list):
        self.coll = self._db[str(strategy_id)]
        outputcursor = self.coll.find({},{"_id":0})
        df = pd.DataFrame(list(outputcursor))
        while True:
            try:
                change_stream = self._db[str(strategy_id)].watch()
                document = next(change_stream)
                df = df.append(document['fullDocument'],ignore_index=True)
                output_payload = self._runind.next(df)
                #output_df.fillna(0)
                #output_payload = output_df.to_json(orient='records',date_format='iso')
                output_format = self.prepare_output_format(output_payload,strategy_id,self._client_id)
                self.payload_contract.insert_data(json.dumps(output_format),strategy_id=strategy_id,db="Indicators")
                #self.output_listener.publish_message(output_format)
            except Exception as e:
                logging.error(f"Exception in listening changes --> {e}")

    def prepare_output_format(self,outputpayload,strategy_id,client_id):
        model = ResponseModel()
        model.event_type = "indicator_output"
        model.client_id = client_id
        model.event_ts = datetime.now().isoformat()
        model.strategy_id = strategy_id
        model.payload = outputpayload
        print({"event_type":model.event_type,"strategy_id":model.strategy_id,"event_ts":model.event_ts,"client_id":model.client_id,"payload":model.payload})
        return {"event_type":model.event_type,"strategy_id":model.strategy_id,"event_ts":model.event_ts,"client_id":model.client_id,"payload":model.payload}
        