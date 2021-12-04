"This is the feeder client and listens for the strategy request"

import asyncio
import logging
import pyfiglet
import os,uuid,json
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from tornado.websocket import websocket_connect
from indicator_response_handler import ResponseHandler

logging.basicConfig(filename="../indicator_clients/logs/indicator_response.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class Indicator_Listener():
    "Feed Listener Class which listens and publishes feed event to the Event Backbone"

    def __init__(self, url, timeout):
        "Initialize listeners and websockets"
        ascii_banner = pyfiglet.figlet_format("Indicator Listener")
        print("---------------------------------------------------------------------------------------------------------")
        print(ascii_banner)
        print("---------------------------------------------------------------------------------------------------------")
        self.url = url
        self.timeout = timeout
        self.ws = None
        self.ioloop = IOLoop.instance()
        self.connect()
        PeriodicCallback(self.keep_alive,20000).start()
        asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
        self.responsehandler = ResponseHandler()

        
        
    @gen.coroutine
    def connect(self):
        "Connect to the WebSocket server"
        logging.info("Connecting to the websocket server")
        try:
            self.ws = yield websocket_connect(self.url)
            print(self.ws)
            self.client_id = str(uuid.uuid4())
            metadata = {"event_type":"metadata","event_producer":"Indicator Listener","client_id":self.client_id,"payload":{"client_id":self.client_id, "client_name":"Indicator Listener"}}
            self.ws.write_message(json.dumps(metadata))
            #dict = {"event_type":"stgy_request", "event_producer":"Strategy1","client_id":self.client_id, "payload": {"feeds":{"ticker":"ICICIBANK","period":"5T","start_date":"2021-01-01 09:00:00","type":"candles"},"indicators":"None"}}
            #self.ws.write_message(json.dumps(dict))
        except Exception as e:
            print(e)
            logging.error(e)
        else:
            logging.info("Connected and running")
            self.run()

    @gen.coroutine
    def get_client_id(self):
        return self.client_id

    
    @gen.coroutine
    def start_loop(self):
        self.ioloop.start()
    
    @gen.coroutine
    def run(self):
        while True:
            contract = self.responsehandler.watchchanges()
            self.ws.write_message(json.dumps(contract))
                
            #   FeedSubscriber()
    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            dict = {"event_type":"keep_alive","event_producer":"Indicator_listener","client_id":self.client_id,"payload":{"type":"keepalive"}}
            self.ws.write_message(json.dumps(dict))


    
if __name__ == '__main__':
     client = Indicator_Listener("ws://localhost:8888/eventsocket",5)
     client.ioloop.start()