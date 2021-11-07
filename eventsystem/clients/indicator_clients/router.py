"Route the indicators to the appriopriate indicator factory"

import logging,json
from dotenv import load_dotenv
import multiprocessing
from indicator_reference import InitiateIndicators
from spawn_strategy_process import SpawnStrategy
from insert_payload import InsertPayload

logging.basicConfig(filename="../indicator_clients/logs/indicator_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
load_dotenv()

class IndicatorRouter():
    "Routes the data to the appropriate indicators"
    def __init__(self):
        "Initialize the indicator routing"
        logging.info("Starting the indicator router")
        self._indicator_dict = {}
        self.ini_ind = InitiateIndicators()
        self._payload_dict = {}
        self._func_list = []
        self._strat_func = {}
        self._is_ind_map = False
        self.spawn_strategy = SpawnStrategy()
        self._insert_payload = InsertPayload()

    def route_message(self,contract):
        "Route the contract appropriately"
        contract_obj = json.loads(contract.decode('utf-8'))

        "Parse the Header"
        _strategy_id = contract_obj['strategy_id']
        _client_id = contract_obj['client_id']
        _payload = contract_obj['payload']
        _eventtype = contract_obj['event_type']

        "Check if this is the indicator request"
        if (_eventtype == 'indicators'):
            self._func_list = self.ini_ind.get_ind_for_strgy(contract)          
            self._strat_func[_strategy_id]  = self._func_list
            logging.info(self._strat_func)
            self.spawn_strategy.start_process(self._strat_func,_strategy_id)
            self._is_ind_map = True
            

        "Check if this is data flow"
        if (_eventtype == 'indicators_data'):
            if self._is_ind_map == True:
                _payload = _payload.replace("\'", "\"")
                self._insert_payload.insert_data(_payload,_strategy_id)
            else:
                logging.error("Indicator Map is not set for the data")
            self._payload_dict[_strategy_id] = _payload