from concurrent_modular_agent import StateClient
import pytest



def test_state_1():
    state = StateClient("agent")
    state.clear()
    assert state.count() == 0
    state.add("aaaa")
    assert state.count() == 1
    
def test_state_2():
    state = StateClient("agent")
    state_num = state.count()
    state.add("aaaa")
    assert state.count() == state_num + 1
    s = state.latest(max_count=10)
    assert s[0].text == "aaaa"

def test_state_3():
    state = StateClient("agent")
    state.clear()
    state.add("concurrent modular agent.")
    state.add("hell world")
    state.add("hogehoge")
    assert state.count() == 3
    s = state.retrieve("agent", max_count=1)
    assert len(s)== 1
    assert s[0].text == "concurrent modular agent."
    
def test_state_4():
    state = StateClient("agent")
    state.clear()
    new_states = []
    for i in range(100):
        new_states.append(f"state {i}")
    state.add(new_states)
    state.add('state new')
    assert state.count() == 101
    s = state.latest(max_count=1)
    assert s[0].text == 'state new'

def test_state_5():
    state = StateClient("agent")
    state.clear()
    s = state.latest()
    assert len(s) == 0

def test_state_6():
    state = StateClient("agent")
    state.clear()
    new_states = []
    for i in range(100):
        new_states.append(f"state {i}")
    state.add(new_states)
    s = state.latest(max_count=-1)
    assert len(s) == 100
