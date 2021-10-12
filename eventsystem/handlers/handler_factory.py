"Factory to return the appropriate Event Handler Objects"

from handlers.strategy_request_handler import StrategyRequestHandler

class HandlerFactory():
    "Handler Factory class to get the objects requested by the router"

    @staticmethod
    def get_handler(request_params,contract):
        "Request for Strategy Handler Object"
        if (request_params == "stgy_request"):
            return StrategyRequestHandler().process(contract=contract)
            
        