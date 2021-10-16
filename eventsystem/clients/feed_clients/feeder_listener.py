"This is the feeder client and listens for the strategy request"

import asyncio
import logging
import pyfiglet
import os,uuid,json
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from tornado.websocket import websocket_connect

logging.basicConfig(filename="../feed_clients/logs/feed_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class FeedListener():
    "Feed Listener Class which listens and publishes feed event to the Event Backbone"

    def __init__(self, url, timeout):
        "Initialize listeners and websockets"
        ascii_banner = pyfiglet.figlet_format("Feed Listener")
        print("---------------------------------------------------------------------------------------------------------")
        print(ascii_banner)
        print("---------------------------------------------------------------------------------------------------------")
        self.url = url
        self.timeout = timeout
        self.ws = None
        self.ioloop = IOLoop.current()
        self.connect()
        PeriodicCallback(self.keep_alive,20000).start()
        asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

        
        
    @gen.coroutine
    def connect(self):
        "Connect to the WebSocket server"
        logging.info("Connecting to the websocket server")
        try:
            self.ws = yield websocket_connect(self.url)
            self.client_id = str(uuid.uuid4())
            metadata = {"event_type":"metadata","event_producer":"Feed Listener","client_id":self.client_id,"payload":{"client_id":self.client_id, "client_name":"Feed Listener"}}
            self.ws.write_message(json.dumps(metadata))
            #dict = {"event_type":"stgy_request", "event_producer":"Strategy1","client_id":self.client_id, "payload": {"feeds":{"ticker":"ICICIBANK","period":"5T","start_date":"2021-01-01 09:00:00","type":"candles"},"indicators":"None"}}
            #self.ws.write_message(json.dumps(dict))
        except Exception as e:
            logging.error(e)
        else:
            logging.info("Connected and running")
            self.run()

    @gen.coroutine
    def get_client_id(self):
        return self.client_id

    @gen.coroutine
    def publish_message(self,contract):
        self.ws.write_message(json.dumps(contract))
    
    @gen.coroutine
    def start_loop(self):
        self.ioloop.start()
    
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
                contract = json.loads(msg)
                
            #    FeedSubscriber()


    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            dict = {"event_type":"keep_alive","event_producer":"Feed_listener","client_id":self.client_id,"payload":{"type":"keepalive"}}
            self.ws.write_message(json.dumps(dict))


    
#if __name__ == '__main__':
 #   client = FeedListener("ws://localhost:8888/eventsocket",5)