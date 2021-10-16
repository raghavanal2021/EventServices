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
        client_id = parse_contract['client_id']
        event_type = parse_contract['event_type']
        payload = parse_contract['payload']
        print(f"Contract is {contract}")
        print(f"Payload is {payload}")
        "Get the Feed Contract Model"
        self._feed_contract_model = RequestModel()
        self._feed_contract_model.client_id = client_id
        self._feed_contract_model.event_type = 'data'
        self._feed_contract_model.payload = json.loads(json.dumps(payload))
        self._feed_payload_model = json.loads(json.dumps(self._feed_contract_model.payload))
        
        "Get the Contract Model"
        self._indicators_contract_model = RequestModel()
        self._indicators_contract_model.client_id = client_id
        self._indicators_contract_model.event_type = 'indicators'
        self._indicators_contract_model.payload = json.loads(json.dumps(payload))
        self._indicators_payload_model = json.loads(json.dumps(self._indicators_contract_model.payload))
        return 100
      
      #      logging.error(f"Error while deserializing contract : {e}")
      #      return -100

    def process(self,contract):
        logging.info("Started to Handle the Strategy Request")
        deserialize_status = self.deserialize_contract(contract=contract)
        if (deserialize_status == 100):
            self._feeds_contract = json.dumps(self._feed_payload_model['feeds'])
            self._indicators_contract = json.dumps(self._indicators_payload_model['indicators'])
            
            self._feed_contract_model.payload = self._feed_payload_model['feeds']
            self._indicators_contract_model.payload = self._indicators_payload_model['indicators']
            
            _feed_serialized_contract = self.serialize_contract(self._feed_contract_model)
            _indicators_serialized_contract = self.serialize_contract(self._indicators_contract_model)

            self._topicpublisher.publish_topic(_feed_serialized_contract,"feeds")
            self._topicpublisher.publish_topic(_indicators_serialized_contract,"indicators")
            return _feed_serialized_contract
        return None
            
    def serialize_contract(self,contract):
        output_contract = {"event_type":contract.event_type, "event_ts":contract.event_ts,
                          "client_id":contract.client_id, "payload":contract.payload}
        print(json.dumps(output_contract))
        return json.dumps(output_contract)
