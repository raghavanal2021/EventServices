"Run Indicator List"
from pymongo import MongoClient
import logging, os,json
from dotenv import load_dotenv
from talib import func
from talib.abstract import Function
import talib

load_dotenv()
logging.basicConfig(filename="../indicator_clients/logs/indicator_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class RunIndicator():
    "This class runs the indicator for the data"

    def __init__(self,strategy_id,indicator_list):
        "Initialize the Change Database and keep the indicator list ready"
        _host = os.getenv("mongohost")
        _port = int(os.getenv("mongoport"))
        self._client = MongoClient(_host,_port)
        self._db = self._client["ChangeDB"]
        self._indfunc = {}
        self._ind_array = self.prepare_indicators(indicator_list=indicator_list,strategy_id=strategy_id)
        self.key_string = ""

    def prepare_indicators(self,strategy_id,indicator_list):
        "Loop through the indicator contract and have the indicator list as a dictionary"
        self._indicator_list = indicator_list[strategy_id]
        for indicators in self._indicator_list:
            _ind = self._indicator_list[indicators].replace("\'","\"")
            print(_ind)
            self._indfunc[indicators] = self._indicator_list[indicators]
            logging.info(f"Indicator list Prepared {self._indfunc}")
        return self._indfunc
    
    def _ta_func(self,fn,df):
        close = df['close']
        open = df['open']
        high = df['high']
        low = df['low']
        volume = df['volume']
        ticker = df['ticker']
        print(f"Function --> {fn}")
        fn_attr = eval(fn)
        return fn_attr

    def next(self,df):
        for ind in self._indfunc:
            print(self._indfunc[ind])
            ind_obj = self._indfunc[ind]
            ticker = df['ticker']
            df = df[(df.ticker == ticker)]
            func_meta = Function(ind).info
            try:
                if len(func_meta['output_names']) > 1:
                    self.key_string = ""
                    for li in func_meta['output_names']:
                        self.key_string = (self.key_string + "," + f"df['{str(li)}']").lstrip(',')
                    exec(f"{self.key_string} = self._ta_func('talib.{ind_obj}',df)")
                else:
                    self.key_string = f"df[{ind}]"
                    df[f"{ind}"] = self._ta_func(f"talib.{ind_obj}",df)
            except Exception as e:
                logging.error(f"Error in calculating the indicators {e}")
        