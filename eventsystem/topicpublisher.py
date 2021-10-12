"This class will publish the client information to the required topic"

import logging
import os
import pika
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class PublishTopic():
    "Get the information from the router and publish the data to the topic"
    def __init__(self) :
        rabbit_host = os.getenv('rabbithost')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
        self.channel = connection.channel()

    def publish(self,message,routing_key):
        exchange = os.getenv("rabbitexchange")
        try:
            self.channel.basic_publish(exchange=exchange,routing_key=routing_key,body=message)
            logging.info(f"Published the message to the clients for consumption")
        except Exception as e:
            logging.error(f"Error in publishing the message. Error is {e}")


