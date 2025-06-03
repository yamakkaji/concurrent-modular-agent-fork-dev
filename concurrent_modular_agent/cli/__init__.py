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

@cli.command()
@click.argument('arg')
def memory(arg):
    """Memory management command"""
    click.echo(f"Not implemented yet. Argument: {arg}")

def main():
    cli()