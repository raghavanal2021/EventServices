"Factory to return the appropriate Event Handler Objects"

from handlers.strategy_request_handler import StrategyRequestHandler
from handlers.indicators_request_handler import IndicatorRequestHandler
class HandlerFactory():
    "Handler Factory class to get the objects requested by the router"
    

    @staticmethod
    def get_handler(request_params,contract):
        "Request for Strategy Handler Object"
        if (request_params == "stgy_request"):
            return StrategyRequestHandler().process(contract=contract)
            
        if (request_params == "data"):
            "Print the Data"
            pass

        if (request_params == "data_load"):
            return IndicatorRequestHandler().process(contract=contract)

      #  if (request_params == "indicator_output"):
      #      return IndicatorRequestHandler().process(contract=contract)
