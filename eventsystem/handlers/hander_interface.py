"This is the interface for handler factory."
from abc import  ABCMeta

class HandlerInterface(metaclass=ABCMeta):
    'Interface for Client Event Handlers'

    @staticmethod
    def process_contract(contract):
        "Proess the contract object"
