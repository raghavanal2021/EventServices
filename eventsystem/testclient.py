"This is a test client for the websocket"

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect
import logging
import json
import pyfiglet
import uuid


logging.basicConfig(filename="./logs/testclient.log",level=logging.INFO,filemode='w',format='%(asctime)s - %(message)s')

class TestClient():
    
    def __init__(self, url, timeout):
        ascii_banner = pyfiglet.figlet_format("Test Client")
        print("---------------------------------------------------------------------------------------------------------")
        print(ascii_banner)
        print("---------------------------------------------------------------------------------------------------------")
        logging.info(ascii_banner)
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive,20000).start()
        self.ioloop.start()
    
    @gen.coroutine
    def connect(self):
        "Connect to the WebSocket server"
        logging.info("Connecting to the websocket server")
        try:
            self.ws = yield websocket_connect(self.url)
            self.client_id = str(uuid.uuid4())
            metadata = {"event_type":"metadata","event_producer":"Strategy1","client_id":self.client_id,"payload":{"client_id":self.client_id, "client_name":"Strategy1"}}
            self.ws.write_message(json.dumps(metadata))
            dict = {"event_type":"stgy_request", "event_producer":"Strategy1","client_id":self.client_id, "payload": {"feeds":{"ticker":"ICICIBANK","period":"5T","start_date":"2021-01-01 09:00:00","type":"candles"},"indicators":"None"}}
            self.ws.write_message(json.dumps(dict))
            dict = {"event_type":"stgy_request", "event_producer":"Strategy2","client_id":self.client_id, "payload": {"feeds":{"ticker":"MOTHERSUMI","period":"5T","start_date":"2021-01-01 09:00:00","type":"candles"},"indicators":"None"}}
            self.ws.write_message(json.dumps(dict))
        except Exception as e:
            logging.error(e)
        else:
            logging.info("Connected and running")
            self.run()

    @gen.coroutine
    def run(self):
        while True: 
            msg = yield self.ws.read_message()
            if msg is None:
                logging.info("Connection closed")
                self.ws = None
                break
            else:
                logging.info(msg)


    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            dict = {"event_type":"keep_alive","event_producer":"Strategy1","client_id":self.client_id,"payload":{"type":"keepalive"}}
            self.ws.write_message(json.dumps(dict))


if __name__ == '__main__':
    client = TestClient("ws://localhost:8888/eventsocket",5)
    