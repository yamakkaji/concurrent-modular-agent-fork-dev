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
    retriever = LatestRetriever()
    s = retriever.retrieve(state, max_count=3)
    assert state.count() == 3
    assert len(s)== 3
    assert s[0].text == "I like cherry."
    assert s[1].text == "I like banana."
    assert s[2].text == "I like apple."

