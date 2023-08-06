import click
from algo_beast_cli.cmd.protocols.initializer import Initializer


@click.command()
@click.argument("project_name")
@click.pass_obj
def pull(obj: Initializer, project_name):
  print(f'pulling {project_name}')
