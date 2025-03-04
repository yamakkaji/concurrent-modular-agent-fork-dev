import multiprocessing
import platform
if platform.system() == 'Darwin':
    multiprocessing.set_start_method('fork')

from concurrent_modular_agent import Agent
from multiprocessing import Queue

def test_module(capfd):
    test_queue = Queue()
    def mod(state, message):
        test_queue.put("module called")
    agent = Agent('myagent')
    agent.add_module("mod", mod)
    agent.start(detach=False)
    assert test_queue.get() == "module called"

    
def test_agent_message():
    send_message = "Hello"
    def sender(state, message):
        message.send("receiver", send_message)
    
    received_message = Queue()
    def receiver(state, message):
        m = message.receive()
        received_message.put(m)
        
    agent = Agent('myagent')
    agent.add_module("receiver", receiver)
    agent.add_module("sender", sender)
    agent.start(detach=False)
    assert received_message.get() == send_message

def test_agent_state():
    def state_add(state, message):
        state.add("test")
        message.send("state_retrieve", "please read state.")
    
    testq = Queue()
    def state_retrieve(state, message):
        message.receive()
        s = state.retrieve("test")
        testq.put(s[0].text)
        
    agent = Agent('myagent')
    agent.add_module("state_retrieve", state_retrieve)
    agent.add_module("state_add", state_add)
    agent.start(detach=False)
    assert testq.get() == "test"
    