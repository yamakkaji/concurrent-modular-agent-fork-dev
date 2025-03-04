import time
from concurrent_modular_agent import Agent, StateClient, MessageClient

def sender(state:StateClient, message:MessageClient):
    i = 0
    while True:
        m = f'hello message {i}'
        print(f'sender: send message {m}')
        message.send("receiver", m)
        i += 1
        time.sleep(1)

def receiver(state:StateClient, message:MessageClient):
    while True:
        m = message.receive()
        print(f'receiver: received message: {m}')
    
agent = Agent('myagent')
agent.add_module("sender", sender)
agent.add_module("receiver", receiver)
agent.start(detach=False)
