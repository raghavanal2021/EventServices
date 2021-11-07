import json
import logging


logging.basicConfig(filename="../indicator_clients/logs/indicator_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
"This class initiates indicator functions for all Technical indicators"
class InitiateIndicators():
    "Creates Indicator Object function and passes the function to the data"

    def __init__(self):
        "Initialize the indicator Strategy Map"
        logging.info("Starting the Indicator list")
        self._ind_stgy_map = {}
        self._stgy_id = None
        self._indicators = None
        self._stgy_type = None
        self._ind_func = {}
        self._childprocess = None


    def get_ind_for_strgy(self,contract):
        logging.info("Parsing Contract")
        result = self._parsecontract(contract)
        if (result == 100):
            print(f"Running for strategy {self._stgy_id} with the indicators {self._indicators}")
            result = self._prepare_ind_func(self._indicators)
            logging.info(f"Indicator functions --> {list(result)}")
            output_list = list(result.values())
            return result
        else:
            logging.error("Error Parsing and geting function list")
            return -100
            

    def _parsecontract(self,contract):
        try:
            contract_obj = json.loads(contract.decode('utf-8'))
            self._stgy_id = contract_obj['strategy_id']
            self._stgy_type = contract_obj['event_type']
            self._indicators = contract_obj['payload']
            return 100
        except Exception as e:
            logging.error(f"Error parsing Contract : {e}")
            return -100

    def _prepare_ind_func(self, ind):
        for indicators in ind:
            indicators = json.loads(str(indicators).replace("\'", "\""))
            _ind_type = indicators["indicator_name"]
            _ind_param = indicators["params"]
            if bool(_ind_param):
                self._ind_bar_name = ""
                self._ind_bar_value = ""
                self._bar_value = ""
                self._param_value = ""
                for params in _ind_param.keys():
                    if params == 'bars':
                        bar_obj = json.loads(str(_ind_param[params]).replace("\'", "\""))
                        for bar_key in bar_obj.keys():
                            if self._ind_bar_name == "":
                                self._ind_bar_name = bar_key
                                self._ind_bar_value = bar_obj[bar_key]
                                self._bar_value = f"{self._ind_bar_value}"
                            else:
                                self._ind_bar_name = bar_key
                                self._ind_bar_value = bar_obj[bar_key]
                                self._bar_value = f"{self._bar_value},{self._ind_bar_value}"
                    else:
                        self._param_value = self._param_value + "," + params + "="+ str(_ind_param[params])
                        self._ind_func[_ind_type] = f"{_ind_type}({self._bar_value} {self._param_value})"
        return self._ind_func
