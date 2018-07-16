import click
from jawa.util.bytecode import opcode_table

from pyjvm import utils
from pyjvm.instructions.instructions import get_implemented_instructions


@click.group()
def cli():
    pass


@click.command()
def instruction_report():
    present_instructions = set(get_implemented_instructions())
    expected_instructions = set(op['mnemonic'] for op in opcode_table.values())
    missing = expected_instructions.difference(present_instructions)
    for key in sorted(missing):
        click.echo(key)

    click.echo(f'{len(present_instructions)} implemented out of {len(expected_instructions)}. Missing: {len(missing)}')


@click.command()
@click.argument('path')
def dump_class(path):
    utils.dump_class(path, click.echo)


cli.add_command(instruction_report)
cli.add_command(dump_class)


def main():
    cli()
