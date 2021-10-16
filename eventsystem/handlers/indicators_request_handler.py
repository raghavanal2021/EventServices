"This will handle all indicators related events"

from handlers.hander_interface import HandlerInterface
from models.requestcontract import RequestModel
from handlers.handler_publishtopic import TopicPublisher
import json,os
import logging

logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class IndicatorRequestHandler(HandlerInterface):

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
        self._feed_contract_model = RequestModel()
        self._indicators_contract_model = RequestModel()
        self._feed_contract_model.client_id = client_id
        self._indicators_contract_model.client_id = client_id
        #self._contract_model.event_ts = parse_contract['event_ts']
        self._feed_contract_model.event_type = 'indicators'
        self._indicators_contract_model.event_type = 'indicators'
        self._feed_contract_model.payload = json.loads(json.dumps(payload))
        self._indicators_contract_model.event_type = json.loads(json.dumps(payload))
        self._feed_payload_model = json.loads(json.dumps(self._feed_contract_model.payload))
        self._indicators_contract_model = json.loads(json.dumps(self._indicators_contract_model.payload))
        return 100
    #      logging.error(f"Error while deserializing contract : {e}")
    #return -100

    def process(self,contract):
        print("Indicators")
        return None
            
    def serialize_contract(self,contract):
        output_contract = {"event_type":contract.event_type, "event_ts":contract.event_ts,
                            "client_id":contract.client_id, "payload":contract.payload}
        print(json.dumps(output_contract))
        return json.dumps(output_contract)
