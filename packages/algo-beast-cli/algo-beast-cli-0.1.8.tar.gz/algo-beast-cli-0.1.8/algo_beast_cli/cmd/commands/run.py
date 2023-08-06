import click
import docker
from algo_beast_cli.cmd.protocols.initializer import Initializer

client = docker.from_env()

@click.command()
@click.argument("project_name")
@click.pass_obj
def run(obj: Initializer, project_name):
  id=1
  client.containers.run("algo-beast-core:latest", "python main.py --id={id} --token={obj.auth.token}", detach=True)
