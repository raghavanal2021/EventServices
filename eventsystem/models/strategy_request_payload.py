"Strategy Request Payload Model"
import json

class Strategy_Request_Payload():
    "Convert and set the Request Payload"
    def __init__(self,payload):
        print(f"Payload --> {payload}")
        self._payload = None
        self._feed_payload = None
        self._indicator_payload = None
        
    def parse_payload(self,payload):
        self._payload = json.loads(payload)
        
        
    def feed_payload(self):
        self._feed_payload = self._payload['feeds']
        

    def indicator_payload(self):
        try:
            self._indicator_payload = self._payload['indicators']
        except Exception as e:
            self._indicator_payload = None
        return None

    def get_feed(self):
        return self._feed_payload

    def get_indicator(self):
        return self._indicator_payload
    

  #  feeds = property(get_feed,feed_payload)
  #  indicators = property(get_indicator,indicator_payload)

        
        