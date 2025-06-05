from concurrent_modular_agent import Agent
from concurrent_modular_agent.state import StateClient
import pytest
import tempfile

def test_memory_list():
    agent = Agent('test_name1')
    state = StateClient("test_name2")
    memory_list = StateClient.get_all_names()
    # for m in memory_list:
        # print(m)
    assert "test_name1" in memory_list, "test_name1 not found in memory list"
    assert "test_name2" in memory_list, "test_name2 not found in memory list"
    # for m in memory_list:
        # print(m)
        
def test_memory_delete():
    state = StateClient("test_name3")
    memory_list = StateClient.get_all_names()
    assert "test_name3" in memory_list, "test_name3 not found in memory list before deletion"    
    
    # Test deletion of an existing memory
    StateClient.delete("test_name3")
    memory_list = StateClient.get_all_names()
    assert "test_name3" not in memory_list, "test_name3 found in memory list after deletion"
    
    # Test deletion of a non-existent memory
    with pytest.raises(ValueError):
        StateClient.delete("test_name3")
        

# def test_memory_backup():
    # state = StateClient("test_name4")
    # state.add("key1", "value1")
    # state.add("key2", "value2")
    # file_path = tempfile.NamedTemporaryFile(delete=False).name
    # utils.backup_memory("test_name4", file_path)