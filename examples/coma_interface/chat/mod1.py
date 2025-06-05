    
import time
import concurrent_modular_agent as coma


@coma.module_main('userinput')
def test2(agent:coma.AgentInterface):
    while True:
        m = input("User: ")
        agent.state.add(f'user_message:{m}')
        agent.message.send("chat", 'reply')  # send signal to chat module
        time.sleep(3)
        