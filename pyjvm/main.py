import click

from pyjvm.execution.execution import get_implemented_instructions


@click.group()
def cli():
    pass


@click.command()
def instruction_report():
    keys = sorted(get_implemented_instructions())
    for key in keys:
        click.echo(key)

    click.echo(f'{len(keys)} implemented')


cli.add_command(instruction_report)


def main():
    cli()

