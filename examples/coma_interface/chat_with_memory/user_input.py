# my_project/agent1/user_input.py
import time
import concurrent_modular_agent as coma

@coma.module_main('user_input')
def mod_user_input(agent: coma.AgentInterface):
    while True:                              # continuously run this module
        m = input("User: ")
        if len(m) == 0 or m.isspace() or m is None:  # if the user input is empty, skip to the next iteration
            continue
        agent.state.add(f"user_message:{m}")
        agent.message.send("chat", "reply to user")  # send message to the "chat" module
        time.sleep(3)                        # wait for 3 seconds before next input