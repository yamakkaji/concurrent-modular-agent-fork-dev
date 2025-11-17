from concurrent_modular_agent import Agent
from concurrent_modular_agent import modules

if __name__ == "__main__":
    agent = Agent('vision_example')
    agent.add_module("vision", 
                     modules.vision(
                         device=0,
                         prompt="Briefly describe the scene in Japanese.",
                         show_window=True,
                     ))
    agent.start(detach=False)
