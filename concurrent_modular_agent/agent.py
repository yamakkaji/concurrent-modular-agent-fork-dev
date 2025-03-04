import multiprocessing, threading
from .state import StateClient
from .message import MessageClient
import concurrent_modular_agent as cma


class Agent():
    def __init__(self, name:str):
        self.name = name
        self.modules = {}
        self.main_process_modules = {}
        self.state = StateClient(self.name)

    def add_module(self, module_name: str, 
                   module_function: callable,
                   main_process: bool = False):
        if main_process:
            raise NotImplementedError("Main process modules are not yet implemented.")
            # self.main_rocess_modules[module_name] = module_function
        else:
            self.modules[module_name] = module_function
    
    def _run_module_process(self, agent_name, module_name, module_function, initialized_bariier):
        state_client = cma.StateClient(agent_name, module_name)
        message_client = cma.MessageClient(agent_name, module_name)
        initialized_bariier.wait()
        module_function(state_client, message_client)
        
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
            
            module_processes.append(process)
            process.start()
        # run main process modules
        for modul_name, module_func in self.main_process_modules.items():
            state_client = cma.StateClient(self.name, module_name)
            message_client = cma.MessageClient(self.name, module_name)
            module_func(state_client, message_client)
            
        if not detach:
            for process in module_processes:
                process.join()
  
        