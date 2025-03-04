import time
from concurrent_modular_agent import Agent, StateClient, MessageClient

# This example is still a work in progress and not yet complete.

def receiver(state:StateClient, message:MessageClient):
    while True:
        m = message.receive()
        print(f'receiver: received message: {m}')
    
agent = Agent('myagent')
agent.add_module("receiver", receiver)
agent.start()
while True:
    m = input("input message: ")
    agent.message.send("receiver", m)
    time.sleep(1)
