import multiprocessing, threading
from .state import StateClient
from .message import MessageClient
import concurrent_modular_agent as cma

"""
This class is intended for the mode where agents are launched via the coma CLI interface.
"""
class AgentInterface:
    def __init__(self, agent_name, module_name):
        self.agent_name = agent_name
        self.module_name = module_name
        self.state = StateClient(agent_name, module_name)
        self.message = MessageClient(agent_name, module_name)


"""
This class is intended for the mode where modules are implemented as Python functions and agents are launched from a Python script.
"""
class Agent():
    def __init__(self, name:str):
        self.name = name
        self.modules = {}
        self.state = StateClient(self.name, 'main')
        self.message = MessageClient(self.name, 'main')

    def add_module(self, module_name: str, 
                   module_function: callable):
        self.modules[module_name] = module_function
    
    @staticmethod
    def _run_module_process(agent_name, module_name, module_function, initialized_bariier):
        if module_function.__code__.co_argcount == 2:
            state_client = cma.StateClient(agent_name, module_name)
            message_client = cma.MessageClient(agent_name, module_name)
            args = (state_client, message_client)
        elif module_function.__code__.co_argcount == 1:
            agent = AgentInterface(agent_name, module_name)
            args = (agent,)
        else:
            raise TypeError(f"{module_function.__name__} must take 1 (AgentInterface) or 2.  (state_client, message_client) arguments, but got {module_function.__code__.co_argcount} arguments.")
        initialized_bariier.wait()
        module_function(*args)
            
        
    def start(self, detach=True):
        module_processes = []
        # run modules
        initialized_bariier = threading.Barrier(len(self.modules))
        # initialized_bariier = multiprocessing.Barrier(len(self.modules))
        for module_name, module_func in self.modules.items():
            # TODO: Use multiprocessing instead of threading, but it's sometime blocking bug with message passing.
            process = threading.Thread(
            # process = multiprocessing.Process(
                target=self._run_module_process, 
                args=(self.name, module_name, module_func, initialized_bariier))
            
            process.daemon = True
            process.start()
            module_processes.append(process)
            
        if not detach:
            for process in module_processes:
                process.join()
  
        