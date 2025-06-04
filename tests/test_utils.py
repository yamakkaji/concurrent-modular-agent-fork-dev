from concurrent_modular_agent import utils, Agent
from concurrent_modular_agent.state import State, StateClient
import pytest

def test_memory_list():
    agent = Agent('test_name1')
    state = StateClient("test_name2")
    memory_list = utils.get_all_memory()
    if "test_name1" not in memory_list:
        assert False, "test_name1 not found in memory list"
    if "test_name2" not in memory_list:
        assert False, "test_name2 not found in memory list"
    # for m in memory_list:
        # print(m)