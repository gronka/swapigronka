import click
import json

from .task_one import task_one


# Note: function names cannot contain digits or underscores

@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def main(ctx, debug):
    """Example"""
    ctx.obj = {}
    ctx.obj["DEBUG"] = debug
    ctx.obj["api_base_url"] = "https://swapi.co/api/"
    click.echo("Click main method invoked:")


@main.command()
@click.pass_context
def go(ctx):
    """Example"""
    click.echo("go for it")


@main.command()
@click.pass_context
def taskone(ctx):
    """"""

    # TODO: we could pass number of chars to get here, but let's not bother for
    # now

    res = task_one(ctx=ctx.obj)

    if ctx.obj["DEBUG"]:
        click.echo(json.dumps(res, indent=4, sort_keys=True))
    else:
        click.echo(json.dumps(res["character_infos"], indent=4, sort_keys=True))
