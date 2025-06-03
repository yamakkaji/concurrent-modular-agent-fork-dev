    
import time
# from test import main
import sys
sys.path.append('..')
from concurrent_modular_agent.cli import module_main
from concurrent_modular_agent.cli import AgentInterface
# import ipdb; ipdb.set_trace()
# sys.path.append('.')
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# import aaa

# @main
@module_main('userinput')
def test2(agent:AgentInterface):
    # print(f'{agent.agent_name}:{agent.module_name} start')
    # i = 0
    while True:
        m = input("User: ")
        agent.state.add(f'user_message:{m}')
        agent.message.send("chat", 'reply')  # send signal to chat module
        time.sleep(3)
        # agent.message.receive()  # wait for signal from chat module        # print(f'mod1:{i}')
        # s = input('user:')
        # print(s)
        # aaa.printx(i)
        # i += 3
        # time.sleep(1)
        
        