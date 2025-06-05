from concurrent_modular_agent import utils, Agent
from concurrent_modular_agent.state import State, StateClient
import pytest

def test_memory_list():
    agent = Agent('test_name1')
    state = StateClient("test_name2")
    memory_list = utils.get_all_memory()
    for m in memory_list:
        print(m)
    assert "test_name1" in memory_list, "test_name1 not found in memory list"
    assert "test_name2" in memory_list, "test_name2 not found in memory list"
    # for m in memory_list:
        # print(m)
        
def test_memory_delete():
    state = StateClient("test_name3")
    memory_list = utils.get_all_memory()
    assert "test_name3" in memory_list, "test_name3 not found in memory list before deletion"    
    
    # Test deletion of an existing memory
    utils.delete_memory("test_name3")
    memory_list = utils.get_all_memory()
    assert "test_name3" not in memory_list, "test_name3 found in memory list after deletion"
    
    # Test deletion of a non-existent memory
    with pytest.raises(ValueError):
        utils.delete_memory("test_name3")