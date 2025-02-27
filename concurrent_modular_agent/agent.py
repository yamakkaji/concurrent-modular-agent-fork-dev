import multiprocessing, threading
from concurrent_modular_agent import message


class Agent():
    def __init__(self, name:str, db_path: str = './db/default'):
        self.db_path = db_path
        self.name = name
        self.modules = {}
        self.messaging_clients = {}

    def add_module(self, module_name: str, module_function: callable):
        self.modules[module_name] = module_function
        
    def _run_modules(self, agent_name, module_name, module_function):
        # state_client = state.StateClient(agent_name, module_name)
        state_client = None
        message_client = message.MessageClient(agent_name, module_name)
        module_function(state_client, message_client)
        
    def start(self, detach=True):
        module_processes = []
        for module_name, module_func in self.modules.items():
            process = threading.Thread(target=self._run_modules, args=(self.name, module_name, module_func))
            # TODO: Use multiprocessing instead of threading, but it's not working with message module
            # process = multiprocessing.Process(target=self._run_modules, args=(self.name, module_name, module_func))
            module_processes.append(process)
            process.start()
        if not detach:
            for process in module_processes:
                process.join()
  
        