from concurrent_modular_agent import StateClient
from concurrent_modular_agent.state import State
from abc import abstractmethod

class BaseRetriever:
    def __init__(self, state: StateClient):
        self.state = state
        
    @abstractmethod
    def retrieve(self, state: StateClient) -> State:
        raise NotImplementedError()


class LatestRetriever(BaseRetriever):
    def retrieve(self, max_count=1):
        latest = self.state.latest(max_count=max_count)
        return latest

class TimeWeightedRetriever(BaseRetriever):
    def __init__(self, state, decay_rate):
        raise NotImplementedError()
        super().__init__(state)
        self.decay_rate = decay_rate
        
    def retrieve(self, query_string:str, max_count=1):
        query_max_count = 100
        all_state, distances = self.state.query(query_string, 
                                                max_count=query_max_count,
                                                return_distances=True)
        import ipdb; ipdb.set_trace()
        