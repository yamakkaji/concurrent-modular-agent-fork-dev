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

