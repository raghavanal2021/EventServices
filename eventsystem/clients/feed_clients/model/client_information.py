"Client Information Model"

class ClientInfo():
    "Get the Client Information"

    def __init__(self):
        self._client_id = None
        self._track_id = None
        self._client_name = 'Feed Listener'

    def set_client_id(self,client_id):
        self._client_id = client_id

    def set_track_id(self,track_id):
        self._track_id = track_id

    def set_client_name(self,client_name):
        self._client_name = client_name

    def get_client_id(self):
        return self._client_id

    def get_track_id(self):
        return self._track_id

    def get_client_name(self):
        return self._client_name

    client_id = property(get_client_id,set_client_id)
    track_id = property(get_track_id,set_track_id)
    client_name = property(get_client_name,set_client_name)