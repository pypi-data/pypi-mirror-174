import click
from algo_beast_cli.cmd.commands.create_project import create_project
from algo_beast_cli.cmd.commands.init import init
from algo_beast_cli.cmd.commands.pull import pull
from algo_beast_cli.cmd.commands.run import run
from algo_beast_cli.cmd.initializer import Initializer


@click.group()
@click.pass_context
def local(ctx):
  ctx.obj = Initializer(ctx)

@local.group()
def cloud():
  pass

local.add_command(init)
local.add_command(create_project)
local.add_command(run)

cloud.add_command(pull)

def main():
  local()

if __name__ == "__main__":
  main()
