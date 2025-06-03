import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import importlib.util
import os
import functools
from concurrent_modular_agent import AgentInterface

def module_main(module_name):
    def _module_main(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            agent = AgentInterface('myagent', module_name)
            return f(agent)
        wrapper.__module_main__ = True
        return wrapper
    return _module_main

def find_module_main_function(script_path):
    spec = importlib.util.spec_from_file_location("module.name", script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = module
    spec.loader.exec_module(module)
    for name, func in module.__dict__.items():
        if callable(func) and getattr(func, "__module_main__", False):
            return func
    return None

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


import click

@click.group()
def cli():
    """CLI tool with run and memory commands"""
    pass

@cli.command()
@click.argument('project_dir')
def run(project_dir):
    """Run the agent with the specified project directory"""
    start_agent(project_dir)

@cli.command()
@click.argument('arg')
def memory(arg):
    """Memory management command"""
    click.echo(f"Not implemented yet. Argument: {arg}")

def main():
    cli()