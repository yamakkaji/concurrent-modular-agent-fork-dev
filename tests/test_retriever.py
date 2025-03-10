from concurrent_modular_agent import StateClient
import pytest

@pytest.fixture
def state():
    state = StateClient("test_timeweighted_retriever")
    state.clear()
    state.add("I like apple.")
    state.add("I like banana.")
    state.add("I like cherry.")
    return state

from concurrent_modular_agent import LatestRetriever
def test_latest_retriever(state):
    retriever = LatestRetriever(state)
    s = retriever.retrieve(max_count=3)
    assert len(s)== 3
    assert s[0].text == "I like cherry."
    assert s[1].text == "I like banana."
    assert s[2].text == "I like apple."

from concurrent_modular_agent import TimeWeightedRetriever
def test_time_weighted_retriever(state):
    return
    retriever = TimeWeightedRetriever(state, decay_rate=0)
    s = retriever.retrieve('cherry', max_count=1)
    assert s[0].text == "I like cherry."
    s = retriever.retrieve('banana', max_count=1)
    assert s[0].text == "I like banana."
