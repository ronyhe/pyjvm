from pathlib import Path

import click
from jawa.cf import ClassFile
from jawa.classloader import ClassLoader
from jawa.util.bytecode import opcode_table

from pyjvm import machine
from pyjvm.actions import Action
from pyjvm.instructions.instructions import get_implemented_instructions
from pyjvm.model.class_loaders import TraditionalLoader
from pyjvm.utils import utils


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
    path = Path(path)
    with path.open(mode='rb') as f:
        cf = ClassFile(f)
        utils.dump_class(cf, click.echo)


@click.command()
@click.argument('path')
@click.argument('name')
def dump_class_from_jar(path, name):
    loader = ClassLoader(path)
    utils.dump_class(loader[name], click.echo)


@click.command()
@click.argument('main_class')
@click.option('-cp', default='')
def run(main_class, cp):
    loader = TraditionalLoader(cp)
    machine.run(loader, main_class)


cli.add_command(action_report)
cli.add_command(instruction_report)
cli.add_command(dump_class)
cli.add_command(dump_class_from_jar)


def main():
    cli()


if __name__ == '__main__':
    main()
