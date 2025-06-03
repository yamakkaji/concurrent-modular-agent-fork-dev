from .state import StateClient
from .message import MessageClient

class AgentInterface:
    def __init__(self, agent_name, module_name):
        self.agent_name = agent_name
        self.module_name = module_name
        self.state = StateClient(agent_name, module_name)
        self.message = MessageClient(agent_name, module_name)
