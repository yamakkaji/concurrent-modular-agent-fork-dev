from ..runner import start_agent
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
