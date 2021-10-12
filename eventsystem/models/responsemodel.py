"Response Model"
import json

class ResponseModel():
    "create, Gets and Sets the Response Model"

    def __init__(self):
        self._event_type = None
        self._event_ts = None
        self._client_id = None
        self._payload = None
        self._track_id = None

    def set_track_id(self,track_id):
        self._track_id = track_id

    def set_event_type(self,event_type):
        self._event_type = event_type

    def set_event_ts(self,event_ts):
        self._event_ts = event_ts

    def set_payload(self,payload):
        self._payload = payload

    def set_client_id(self,client_id):
        self._client_id = client_id

    def get_track_id(self):
        return self._track_id

    def get_event_type(self):
        return self._event_type

    def get_event_ts(self):
        return self._event_ts

    def get_payload(self):
        return self._payload

    def get_client_id(self):
        return self._client_id

    event_type = property(get_event_type,set_event_type)
    payload = property(get_payload,set_payload)
    event_ts = property(get_event_ts,set_event_ts)
    client_id = property(get_client_id,set_client_id)
    track_id = property(get_track_id,set_track_id)