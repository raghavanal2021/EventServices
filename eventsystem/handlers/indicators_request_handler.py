"This will handle all indicators related events"

from handlers.handler_interface import HandlerInterface
from models.requestcontract import RequestModel
from handlers.handler_publishtopic import TopicPublisher
import json,os
import logging

logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',format='%(levelname)s : %(filename)s -%(asctime)s - %(message)s')
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
        strategy_id = parse_contract['strategy_id']
        payload = parse_contract['payload']
        self._indicators_contract_model = RequestModel()
        self._indicators_contract_model.client_id = client_id
        self._indicators_contract_model.strategy_id = strategy_id
        if event_type == 'data_load':
            self._indicators_contract_model.event_type = 'indicators_data'
        self._indicators_contract_model.payload = payload
        return 100
    
    def process(self,contract):
        _deserialize_status = self.deserialize_contract(contract=contract)
        if _deserialize_status == 100 :
             output_obj = self.serialize_contract(self._indicators_contract_model)
             self._topicpublisher.publish_topic(output_obj,'indicators')
        else:
            logging.error("Deserialization Failed")
        return None
            
    def serialize_contract(self,contract):
        output_contract = {"event_type":contract.event_type, "event_ts":contract.event_ts,"strategy_id":contract.strategy_id,
                            "client_id":contract.client_id, "payload":contract.payload}
        return json.dumps(output_contract)
