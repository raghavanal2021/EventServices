"This class uses aio-pika to connect to the event system and read the messages from the topic"

import logging
import os
import asyncio
import aio_pika
from aio_pika.pool import T, Pool
from aio_pika.robust_connection import connect_robust
from dotenv import load_dotenv
from router import MessageRouter
import pyfiglet
import threading

logging.basicConfig(filename="../feed_clients/logs/feed_subscriber.log",level=logging.INFO,filemode='w',
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
        exchange = await channel.declare_exchange("direct")

        "Declare the queue"
        queue = await channel.declare_queue(queue_name)

        "Bind the queue"
        exchange = os.getenv("rabbitexchange")
        await queue.bind(exchange=exchange,routing_key=routing_key)
        logging.info("Queue Binding Successful")
    except Exception as e:
        logging.error(f"Unable to create channel or bind to the queue {e}")
    
    "Receive the message"
    while True:
            try:
                incoming_message = await queue.get()
                message = incoming_message.body
                incoming_message.ack() 
                print(message)
                start_thread(message)
            except asyncio.QueueEmpty:
                pass
def start_thread(message):
      print("Starting Thread")
      messagerouter = MessageRouter()
      t = threading.Thread(target=messagerouter.route_message,args=[message],daemon=True)
      message_threads.append(t) 
      t.start()
      

if __name__ == '__main__':
        ascii_banner = pyfiglet.figlet_format("Feed Subscriber")
        print("---------------------------------------------------------------------------------------------------------")
        print(ascii_banner)
        print("---------------------------------------------------------------------------------------------------------")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop))