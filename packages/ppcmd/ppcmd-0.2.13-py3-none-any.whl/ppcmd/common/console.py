import click


def echo__(msg):
    print(msg)
    return msg + "\n"


def print_cyan__(msg):
    click.echo(click.style("  :" + msg, fg="cyan"))
