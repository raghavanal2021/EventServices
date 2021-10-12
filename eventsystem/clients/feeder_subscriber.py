"Feed Subscriber from Event Backbone"
import pika
import sys


class Feed_Subscriber():
    
    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self._channel = connection.channel()
        self._channel.exchange_declare(exchange='eventexchange',exchange_type='direct')
    