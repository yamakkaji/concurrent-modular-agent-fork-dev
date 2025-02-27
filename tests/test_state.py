from concurrent_modular_agent import StateClient
import pytest



def test_state_1():
    state = StateClient("agent")
    state.clear()
    assert state.count() == 0
    state.put("aaaa")
    assert state.count() == 1
    
def test_state_2():
    state = StateClient("agent")
    state.put("aaaa")
    s = state.get(max_count=10)
    assert len(s) == 1
    assert s[0] == 'aaaa'


    
    