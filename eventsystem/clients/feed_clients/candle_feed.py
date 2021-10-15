"This is the candle Feed Implementation Class"
import logging
import os,json
from pymongo import MongoClient
import time
import pymongo
from dotenv import load_dotenv
from datetime import datetime, time,timedelta
from model.responsemodel import ResponseModel

from tornado.gen import sleep

load_dotenv()
logging.basicConfig(filename="../feed_clients/logs/feed_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class CandleFeed():
    "This class provides the candle feed for the requested contract"

    def __init__(self):
        "Initialize the Mongo Database and get the Mongo Client"
        mongohost = os.getenv("mongohost")
        mongoport = int(os.getenv("mongoport"))
        try:
            self._mongoclient = MongoClient(mongohost,mongoport)
            self.mongo_db = self._mongoclient['MinuteData']
            logging.info("Successfully connected to Mongo Server")
        except Exception as e:
            logging.error(f"Error Connecting to MongoDB {e}")

    async def get_feed(self,start_date,period,ticker,client_id):
        self._mongo_coll = self.mongo_db[ticker]
        startdate = datetime.strptime(start_date,"%Y-%m-%d %H:%M:%S")
        enddate = timedelta(days=1) + startdate
        logging.info(f"Starting the feed for {ticker} with start date {startdate} and end date {enddate}")
        _output_cursor = self._mongo_coll.find({'timestamp':{'$gt':startdate,'$lt': enddate}},{ "_id": 0}).sort('timestamp',pymongo.ASCENDING)
        _output_list = list(_output_cursor)
        _output_json_list = []
        for data in _output_list:
            _output = self.prepare_output_format(data,client_id)
            _output_json_list.append(_output)
       # print(_output_json_list)
        return _output_json_list

    def prepare_output_format(self,data,client_id):
        self._responsemodel = ResponseModel()
        self._responsemodel.event_type = 'data_load'
        self._responsemodel.event_ts = str(datetime.now().isoformat())
        self._responsemodel.payload = str(data)
        self._responsemodel.client_id = client_id
        return {"event_type":self._responsemodel.event_type,"event_ts":self._responsemodel.event_ts,"client_id":self._responsemodel.client_id,"payload":self._responsemodel.payload}