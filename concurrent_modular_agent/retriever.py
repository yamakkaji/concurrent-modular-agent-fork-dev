from concurrent_modular_agent import StateClient
from concurrent_modular_agent.state import State
from abc import abstractmethod
import numpy as np
from datetime import datetime

class BaseRetriever:
    def __init__(self, state: StateClient):
        self.state = state
        
    @abstractmethod
    def retrieve(self, state: StateClient) -> State:
        raise NotImplementedError()


class LatestRetriever(BaseRetriever):
    def retrieve(self, max_count=1):
        latest = self.state.get(max_count=max_count)
        return latest

class OldestRetriever(BaseRetriever):
    def retrieve(self, max_count=1):
        oldest = self.state.get(max_count=max_count, reverse=True)
        return oldest

class TimeWeightedRetriever(BaseRetriever):
    def __init__(self, state, decay_rate):
        super().__init__(state)
        self.decay_rate = decay_rate
        
    def retrieve(self, 
                 query_text:str, 
                 max_count=1, 
                 now:float|datetime=None):
        query_max_count = 100
        all_state, distances = self.state.query(query_text, 
                                                max_count=query_max_count,
                                                return_distances=True)
        if now is None:
            now = datetime.now().timestamp()
        if type(now) == datetime:
            now = now.timestamp()
        
        distances = np.array(distances)
        time_diff = now - np.array(all_state.timestamps)
        timeweighted_distances = distances * np.exp(time_diff*self.decay_rate) # exponential cecay
        # TODO: Implement linear decay
        # timeweighted_distances = distances * (1 + time_diff*self.decay_rate)   # linear decay
        index = np.argsort(timeweighted_distances)
        timeweighted_states = all_state[index]
        if max_count is not None and max_count > 0:
            timeweighted_states = timeweighted_states[:max_count]
        return timeweighted_states

        
        
        
        
        