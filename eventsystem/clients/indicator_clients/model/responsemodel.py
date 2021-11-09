"Request Model"

class ResponseModel():
    "create, Gets and Sets the Response Model"

    def __init__(self):
        self._event_type = None
        self._event_ts = None
        self._client_id = None
        self._payload = ""
        self._strategy_id = None
        self._ticker = None

    def set_ticker(self,ticker):
        self._ticker = ticker

    def set_event_type(self,event_type):
        self._event_type = event_type

    def set_event_ts(self,event_ts):
        self._event_ts = event_ts

    def set_payload(self,payload):
        self._payload = payload

    def set_client_id(self,client_id):
        self._client_id = client_id
    
    def set_strategy_id(self,strategy_id):
        self._strategy_id = strategy_id

    def get_ticker(self):
        return self._ticker

    def get_event_type(self):
        return self._event_type

    def get_event_ts(self):
        return self._event_ts

    def get_payload(self):
        return self._payload

    def get_client_id(self):
        return self._client_id

    def get_strategy_id(self):
        return self._strategy_id        

    event_type = property(get_event_type,set_event_type)
    payload = property(get_payload,set_payload)
    event_ts = property(get_event_ts,set_event_ts)
    client_id = property(get_client_id,set_client_id)
    strategy_id = property(get_strategy_id,set_strategy_id)
    ticker = property(get_ticker, set_ticker)
