"This class uses aio-pika to connect to the event system and read the messages from the topic"

import logging
import os
import asyncio
from aio_pika import connect_robust
from aio_pika.exchange import ExchangeType
from aio_pika.message import IncomingMessage
from dotenv import load_dotenv
#from router import MessageRouter
import pyfiglet
import threading,json
from router import IndicatorRouter

logging.basicConfig(filename="../indicator_clients/logs/indicator_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
load_dotenv()
ind = IndicatorRouter()

async def on_message(message:IncomingMessage):
    "Process on every message"
    with message.process():
       ind.route_message(contract=message.body)

async def main(loop):
    "Start the connection"
    rabbit_url = os.getenv("rabbiturl")
    connection = await connect_robust(rabbit_url,loop=loop)

    "Create a Channel"
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    "Declare an exchange"
    rabbit_exchange = os.getenv("rabbitexchange")
    exchange = await channel.declare_exchange(rabbit_exchange,ExchangeType.DIRECT,durable=True)

    "Declare a queue and bind to exchange"
    rabbit_queue = os.getenv("queuename")
    routing_key = os.getenv("routingkey")
    queue = await channel.declare_queue(rabbit_queue)
    await queue.bind(rabbit_exchange,routing_key=routing_key)

    "Start Listening to queue"
    await queue.consume(on_message)

if __name__ == '__main__':
        ascii_banner = pyfiglet.figlet_format("Indicators")
        print("---------------------------------------------------------------------------------------------------------")
        print(ascii_banner)
        print("---------------------------------------------------------------------------------------------------------")
        loop = asyncio.get_event_loop()
        loop.create_task(main(loop))
        loop.run_forever()