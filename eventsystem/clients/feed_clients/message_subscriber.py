from router import MessageRouter

class MessageSubscriber:

    def __init__(self,name):
        self.name = name

    def update(self,message):
        router = MessageRouter()
        router.route_message(message)