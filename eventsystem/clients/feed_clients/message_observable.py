"Subject acknowledges the message received from the queue and directs to the router"

import logging
from router import MessageRouter

logging.basicConfig(filename="../feed_clients/logs/feed_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')

class MessageObservable():

    def __init__(self):
        self.msg_object = None
        self.subscribers = set()
        logging.info("Starting the Observer")

    def register(self,who):
        self.subscribers.add(who)

    def unregister(self,who):
        self.subscribers.discard(who)

    async def dispatch(self,message):
        for subscriber in self.subscribers:
            await subscriber.update(message)
            