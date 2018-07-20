import click
from jawa.util.bytecode import opcode_table

from pyjvm import utils
from pyjvm.actions import Action
from pyjvm.instructions.instructions import get_implemented_instructions


@click.group()
def cli():
    pass


@click.command()
def instruction_report():
    present_instructions = set(get_implemented_instructions())
    expected_instructions = set(op['mnemonic'] for op in opcode_table.values())
    missing = expected_instructions.difference(present_instructions)
    invented = present_instructions.difference(expected_instructions)

    click.echo(f'{len(present_instructions)} implemented out of {len(expected_instructions)}. Missing: {len(missing)}')

    for key in sorted(missing):
        click.echo(key)

    click.echo(f'\n{len(invented)} invented instructions')


@click.command()
def action_report():
    names = Action.action_names()
    click.echo(f'{len(names)} commands:')
    for name in names:
        click.echo(name)


@click.command()
@click.argument('path')
def dump_class(path):
    utils.dump_class(path, click.echo)


cli.add_command(action_report)
cli.add_command(instruction_report)
cli.add_command(dump_class)


def main():
    cli()
