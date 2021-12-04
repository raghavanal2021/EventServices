"This routes the messages to the message publisher"
import logging
import json,time
from candle_feed import CandleFeed
from feeder_listener import FeedListener
from handler_publishtopic import TopicPublisher
import asyncio,ast

logging.basicConfig(filename="../feed_clients/logs/feed_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class MessageRouter():
    "This class routes the message to the appropriate message handler to get the message"

    def __init__(self):
        self._candlefeed = CandleFeed()
        logging.info("Started to route the message request to the message handler")
        self.output_listener = FeedListener("ws://localhost:8888/eventsocket",5)
        self.subscribers = set()
        self._publish = TopicPublisher()

    def route_message(self,contract):
        #contract_json = json.dumps(str(contract.decode('utf-8')))
        #print(contract_json)
        print(contract.decode('utf-8'))
        #self.register(contract)
        contract_obj = json.loads(contract.decode('utf-8'))
        print(contract_obj)
        _event_type = contract_obj["event_type"]
        _client_id = contract_obj['client_id']
        _strategy_id = contract_obj['strategy_id']
        _payload = contract_obj['payload']
        payload_contract = json.loads(json.dumps(_payload))
        type = payload_contract['type']
        start_date = payload_contract['start_date']
        period = payload_contract['period']
        ticker = payload_contract['ticker']
       # client_id = contract_obj['client_id']
        if type == 'candles':
            logging.info(f"Identified the type as {type} and calling the {type} feed")
            _outputfeed = self._candlefeed.get_feed(start_date=start_date,period=period,ticker=ticker,client_id=_client_id,strategy_id = _strategy_id)
            for feeds in _outputfeed:
                self.output_listener.publish_message(feeds)
                self.frontend_publish(feeds)
                time.sleep(0.5)
        return "Success"

    def frontend_publish(self,contract):
        ctrct = json.loads(json.dumps(contract))
        payloadcontract = ast.literal_eval(ctrct["payload"])
        print(json.dumps(payloadcontract))
        self._publish.publish_to_topic(json.dumps(payloadcontract),'frontend')
        return 0
        