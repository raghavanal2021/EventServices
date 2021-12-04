"Listen to Mongo Database Changes"
from datetime import datetime
import logging, os
import json, pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import pandas as pd
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware



load_dotenv()
logging.basicConfig(filename="../indicator_clients/logs/indicator_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
_host = os.getenv("mongohost"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           )
_port = int(os.getenv("mongoport"))
try:
    _client = MongoClient(_host,_port)
    _db = _client["frontend"]
except Exception as e:
    logging.error(f"Exception in listening for changes --> {e} ")
        
        
        #self.dataframe = pd.DataFrame(columns=['timestamp','open','high','low','close','volume','ticker'],index=['timestamp'])
@app.websocket("/ws")
async def watchchanges(websocket:WebSocket):
    coll = _db["pricedata"]
    outputcursor = coll.find({},{"_id":0})
    df = pd.DataFrame(list(outputcursor))
    while True:
        try:
            change_stream = _db["pricedata"].watch()
            document = next(change_stream)
            print(document)
            await websocket.send_text(document)
        except KeyboardInterrupt :
            logging.info("Interrupted!! Exiting")
        
            
