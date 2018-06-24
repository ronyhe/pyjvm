import click

from pyjvm.execution.execution import get_implemented_instructions


@click.command()
def instruction_report():
    keys = sorted(get_implemented_instructions())
    for key in keys:
        click.echo(key)

    click.echo(f'{len(keys)} implemented')


if __name__ == '__main__':
    instruction_report()
