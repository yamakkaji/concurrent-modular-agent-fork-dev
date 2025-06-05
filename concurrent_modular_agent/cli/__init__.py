import click


@click.group()
def cli():
    """CLI tool for concurrent modular agent"""
    pass


"""
Run commands
"""
from ..agent_runner import start_agent

@cli.command()
@click.argument('project_dir')
def run(project_dir):
    """Run the agent with the specified project directory"""
    start_agent(project_dir)


"""
Backend commands
"""
from .. import backend as coma_backend

@cli.group()
def backend():
    """Backend management commands"""
    pass

@backend.command()
def start():
    """Start the backend service"""
    coma_backend.start()

@backend.command()
def stop():
    """Stop the backend service"""
    coma_backend.stop()

@backend.command()
def restart():
    """Restart the backend service"""
    coma_backend.stop()
    coma_backend.start()


"""
Memory commands
"""    
from .. import utils as coma_utils

@cli.group()
def memory():
    """Memory management commands"""
    pass

@memory.command()
def ls():
    """List memory contents"""
    memory_list = coma_utils.get_all_memory()
    for memory in memory_list:
        print(memory)

@memory.command()
@click.argument('name')
def rm(name):
    """Delete memory with the specified name"""
    try:
        coma_utils.delete_memory(name)
        print(f"Memory '{name}' deleted successfully.")
    except ValueError as e:
        print(e)

def main():
    cli()
