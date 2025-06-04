from ..agent_runner import start_agent
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
@cli.group()
def memory():
    """Memory management commands"""
    pass

@memory.command()
def ls():
    """List memory contents"""
    click.echo("Memory ls command - not implemented yet")

def main():
    cli()
