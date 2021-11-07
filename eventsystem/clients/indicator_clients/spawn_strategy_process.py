"Spawn Strategy Process"
import threading
import signal
import logging
from listen_mongo_changes import Listen_Changes

logging.basicConfig(filename="../indicator_clients/logs/indicator_subscriber.log",level=logging.INFO,filemode='w',
                    format='%(levelname)s : %(name)s -%(asctime)s - %(message)s')
class SpawnStrategy():
    "This class spawns process per strategy. The target process will listen to MongoDB change streams for processing"

    def __init__(self):
        self._thread = None
        self._error_flags = False
        self.threads = []
    
    def child_process_meta(self,indicator_list,strategy_id):
        logging.info(f"Child Thread is being processed for strategy id {strategy_id}")
        logging.info(f"Indicator List {indicator_list}")
        self._listener = Listen_Changes(strategy_id=strategy_id,indicator_list=indicator_list)
        self._listener.watchchanges(strategy_id=strategy_id,indicator_list=indicator_list)

    def start_process(self,indicator_list,strategy_id):
        self._thread = threading.Thread(target=self.child_process_meta,args=(indicator_list,strategy_id),daemon=True)
        self.threads.append(self._thread)
        self._thread.start()