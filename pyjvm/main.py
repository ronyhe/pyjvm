"""The command line gateway to the system

This module uses the click library (http://click.pocoo.org) to provide the following commands:
 - ``pyjvm instruction_report``: Displays information regarding the system's support for jvm instructions.
 - ``pyjvm action_report``: Displays the Action sub classes that exist in the system
 - ``pyjvm dump_class``: Displays ClassFile information that proves helpful during development.
   Compliments the javap functionality
 - ``pyjvm dump_class_from_jar``: Similar to dump_class but provides the ability to inspect classes inside JAR files
 - ``pyjvm run``: Runs a JVM class.
   Provides classpath functionality via an argument.
   Provides basic tracing ability via a flag.
"""
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
    """The main command

    This command exists as a grouper for the other commands, which is why all other commands are sub-commands
    of pyjvm.
    """
    pass


@click.command()
def instruction_report():
    """A command that displays information regarding the instruction set

        - How many commands are expected (exist in the spec)?
        - How many of them are implemented?
        - How many are missing, and what are their names?
        - Do we have inadvertent instructions that don't exist in the spec?

        .. code::

            pyjvm instruction_report
            205 implemented out of 205. Missing: 0
            0 invented instructions
    """
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
    """A command that displays the :class:`Action` types that exist in the system"""
    names = Action.action_names()
    click.echo(f'{len(names)} commands:')
    for name in names:
        click.echo(name)


@click.command()
@click.argument('path')
def dump_class(path):
    """A command that displays useful information that exists in a class file

    A compliment to the JDK `javap` program.
    """
    path = Path(path)
    with path.open(mode='rb') as f:
        cf = ClassFile(f)
        utils.dump_class(cf, click.echo)


@click.command()
@click.argument('path')
@click.argument('name')
def dump_class_from_jar(path, name):
    """A command that displays useful information that exists in a class that is inside a JAR

    Similar to `dump_class`
    """
    loader = ClassLoader(path)
    utils.dump_class(loader[name], click.echo)


@click.command()
@click.argument('main_class')
@click.option('-cp', default='')
@click.option('--report', is_flag=True)
def run(main_class, cp, report):
    """A command that executes a `main` method in a JVM class

    :param main_class: The name of the class
    :param cp: Colon separated class anf jar files
    :param report: A bool representing whether or not to dump execution info to stdout
    """
    loader = TraditionalLoader(cp)
    if report:
        echo = print
    else:
        echo = None
    machine.run(loader, main_class, echo=echo)


# Add the sub commands to the main command, as per the `click` documentation
cli.add_command(run)
cli.add_command(action_report)
cli.add_command(instruction_report)
cli.add_command(dump_class)
cli.add_command(dump_class_from_jar)


def main():
    cli()


if __name__ == '__main__':
    main()
