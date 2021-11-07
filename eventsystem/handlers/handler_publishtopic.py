"This will publish to the topic for Publish Subscribe Model"

import logging
import pika
import os
import json

from pika import exchange_type
logging.basicConfig(filename="./logs/eventbackbone.log",level=os.getenv("loglevel"),filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class TopicPublisher():
    "This class instantiates topic object and publishes the data and indicator to the strategy"

    def __init__(self):
        "Initialize the Rabbit MQ class"
        rabbithost = os.getenv("rabbithost")
        self.rabbitexchange = os.getenv("rabbitexchange")
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host= rabbithost))
            self.channel = connection.channel()
        except Exception as e:
            logging.error(f"Error while establishing Rabbit MQ {e}")
            

    def publish_topic(self,message,routing_key):
        "Publish to the required routing"
        try:
            self.channel.exchange_declare(exchange=self.rabbitexchange,exchange_type='direct',durable=True)
            self.channel.basic_publish(exchange=self.rabbitexchange, routing_key=routing_key,body=message)
            logging.info(f"Published to the event")
            return json.dumps({"status_code":100, "status_desc":"Routing succeeded"})
        except Exception as e:
            logging.error(f"Error while publishing the topic {e}")
            return json.dumps({"status_code":-100, "status_desc": e})
