"This will handle all Strategy Requests and provide response to the routers "

from handlers.hander_interface import HandlerInterface
from models.requestcontract import RequestModel
from handlers.handler_publishtopic import TopicPublisher
import json,os
import logging

logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class StrategyRequestHandler(HandlerInterface):

    def __init__(self):
        self._contract_model = None
        self._payload_model = None
        self._feeds_contract = None
        self._indicators_contract= None
        self._topicpublisher = TopicPublisher()

    def deserialize_contract(self,contract):
        parse_contract = json.loads(json.dumps(contract))
        self._contract_model = RequestModel()
        self._contract_model.client_id = parse_contract['client_id']
        # self._contract_model.event_ts = parse_contract['event_ts']
        self._contract_model.event_type = parse_contract['event_type']
        self._contract_model.payload = parse_contract['payload']
        self._payload_model = json.loads(json.dumps(self._contract_model.payload))
        return 100
      
      #      logging.error(f"Error while deserializing contract : {e}")
      #      return -100

    def process(self,contract):
        logging.info("Started to Handle the Strategy Request")
        deserialize_status = self.deserialize_contract(contract=contract)
        if (deserialize_status == 100):
            self._feeds_contract = json.dumps(self._payload_model['feeds'])
            self._indicators_contract = json.dumps(self._payload_model['indicators'])
            self._topicpublisher.publish_topic(self._feeds_contract,"feeds")
            self._topicpublisher.publish_topic(self._indicators_contract,"indicators")
            _contract = {"feeds": self._feeds_contract, "indicators": self._indicators_contract}
            _serialized_contract = self.serialize_contract(_contract)
            return _serialized_contract
        return None
            
    def serialize_contract(self,contract):
        output_contract = json.dumps(contract)
        return output_contract
