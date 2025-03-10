from concurrent_modular_agent import StateClient
from concurrent_modular_agent.state import State
import numpy as np
import pytest


def test_state_0():
    ids = ["id0", "id1", "id2", "id3", "id4"]
    texts = ["text0", "text1", "text2", "text3", "text4"]
    vector = np.random.rand(5, 10)  # 5つの10次元ベクトル
    timestamps = [0.0, 1.0, 2.0, 3.0, 4.0]
    state = State(ids, texts, vector, timestamps)
    assert state[1].text == "text1"
    assert len(state[[1, 3, 4]]) == 3
    assert state[[1, 3, 4]][1].text == "text3"

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
    s = state.query("agent", max_count=1)
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
    s = state.latest(max_count=None)
    assert len(s) == 100

import datetime
def test_state_datetime_1():
    state = StateClient("agent")
    state.clear()
    state.add("3", timestamp=datetime.datetime(2025, 1, 3))
    state.add("1", timestamp=datetime.datetime(2025, 1, 1))
    state.add("2", timestamp=datetime.datetime(2025, 1, 2))
    s = state.latest(max_count=3)
    assert s[0].text == "3"
    assert s[1].text == "2"
    assert s[2].text == "1"

def test_state_datetime_2():
    state = StateClient("agent")
    state.clear()
    state.add("3", timestamp=3)
    state.add("1", timestamp=1)
    state.add("2", timestamp=2)
    s = state.latest(max_count=3)
    assert s[0].text == "3"
    assert s[1].text == "2"
    assert s[2].text == "1"    