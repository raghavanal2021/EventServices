"This class uses aio-pika to connect to the event system and read the messages from the topic"

import logging
import os
import asyncio
import aio_pika
from aio_pika.pool import T, Pool
from aio_pika.robust_connection import connect_robust
from dotenv import load_dotenv
from routetoserver import Router
import pyfiglet
import threading

logging.basicConfig(filename="../frontend_clients/logs/frontend_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
load_dotenv()


message_threads = []

async def main(loop):
    rabbit_url = os.getenv("rabbiturl")
    try:
        connection = await connect_robust(rabbit_url,loop=loop)
        logging.info("RabbitMQ Connection Successful")
    except Exception as e:
        logging.error(f"Error connecting to Rabbit MQ {e}")
    queue_name = os.getenv("queuename")
    routing_key = os.getenv("routingkey")
    try:
        "Create the Channel"
        channel = await connection.channel()

        "Declare the exchange"
        exchange = await channel.declare_exchange("topic")

        "Declare the queue"
        queue = await channel.declare_queue(queue_name)

        "Bind the queue"
        exchange = os.getenv("rabbittopicexchange")
        await queue.bind(exchange=exchange,routing_key=routing_key)
        logging.info("Queue Binding Successful")
    except Exception as e:
        logging.error(f"Unable to create channel or bind to the queue {e}")
    
    "Receive the message"
    while True:
            try:
                incoming_message = await queue.get()
                message = incoming_message.body
                print(message.decode('utf-8'))
                incoming_message.ack() 
            except asyncio.QueueEmpty:
                pass

if __name__ == '__main__':
        ascii_banner = pyfiglet.figlet_format("Frontend Subscriber")
        print("---------------------------------------------------------------------------------------------------------")
        print(ascii_banner)
        print("---------------------------------------------------------------------------------------------------------")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop))