import socketio
from aiohttp import web
from pymongo import MongoClient
import os,logging
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()
logging.basicConfig(filename="../indicator_clients/logs/indicator_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')

sio = socketio.AsyncServer(async_mode='asgi',cors_allowed_origins=['http://localhost:4200'])
app = socketio.ASGIApp(sio)

#sio.attach(app)

_host = os.getenv("mongohost")
_port = int(os.getenv("mongoport"))
try:
    _client = MongoClient(_host,_port)
    _db = _client["frontend"]
except Exception as e:
    logging.error(f"Exception in listening for changes --> {e} ")


@sio.event
def connect(sid,environ,auth):
    print("Socket ID: ", sid )

@sio.event
async def start(sid,msg):
    print(msg)
    coll = _db["pricedata"]
    outputcursor = coll.find({},{"_id":0})
    df = pd.DataFrame(list(outputcursor))
    status = True
    try:
        while status==True:
            change_stream = _db["pricedata"].watch()
            document = next(change_stream)
            doc = document['fullDocument']
            doc.pop("_id")
            doc1 = json.dumps(doc)
            await sio.emit('frontend',doc1)
    except KeyboardInterrupt as e:
            logging.warning("Keyboard exit")        
            status = False
    except Exception as e:
            logging.error(f"Exception in listening changes --> {e}")
            

if __name__ == '__main__':
    app.run()
    
    