"""Concurrent Module Agent"""

__version__ = "0.0.4"

import multiprocessing, platform
# if platform.system() == 'Darwin':
    # multiprocessing.set_start_method('fork')
    
from .agent import Agent, AgentInterface
from .message import MessageClient
from .state import StateClient
from .retriever import BaseRetriever, LatestRetriever, OldestRetriever, TimeWeightedRetriever
from .agent_runner import module_main
