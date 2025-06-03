import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
# import importlib.util
import os
# import functools
# from concurrent_modular_agent import AgentInterface
from .module_runner import find_module_main_function


class ScriptReloader(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None
        self.restart_script()

    def restart_script(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        # print(f"Starting script: {self.script_path}")
        self.process = subprocess.Popen([sys.executable, '-m' 'concurrent_modular_agent.module_runner', self.script_path])

    def on_modified(self, event):
        print(f"Detected change in {self.script_path}")
        if event.src_path == os.path.abspath(self.script_path):
            self.restart_script()

import glob

def start_agent(project_dir):
    script_paths = glob.glob(f"{project_dir}/*.py", recursive=True)
    watchdog_observers = []
    watchdog_event_handlers = []
    for script_path in script_paths:
        if find_module_main_function(script_path) is None:
            continue
        event_handler = ScriptReloader(script_path)
        observer = Observer()
        observer.schedule(event_handler, path=os.path.abspath(script_path), recursive=False)
        observer.start()
        watchdog_event_handlers.append(event_handler)
        watchdog_observers.append(observer)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for event_handler in watchdog_event_handlers:
            event_handler.process.terminate()
            event_handler.process.wait()
        for observer in watchdog_observers:
            observer.stop()
        for observer in watchdog_observers:
            observer.join()

