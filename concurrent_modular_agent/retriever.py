from concurrent_modular_agent import StateClient
from abc import abstractmethod

class BaseRetriever:
    @abstractmethod
    def retrieve(self, state: StateClient):
        raise NotImplementedError()

class LatestRetriever(BaseRetriever):
    def retrieve(self, state: StateClient, max_count=1):
        latest = state.latest(max_count=max_count)
        return latest
