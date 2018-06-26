import click

from pyjvm import utils
from pyjvm.instructions.instructions import get_implemented_instructions


@click.group()
def cli():
    pass


@click.command()
def instruction_report():
    keys = sorted(get_implemented_instructions())
    for key in keys:
        click.echo(key)

    click.echo(f'{len(keys)} implemented')


@click.command()
@click.argument('path')
def dump_class(path):
    utils.dump_class(path, click.echo)


cli.add_command(instruction_report)
cli.add_command(dump_class)


def main():
    cli()
