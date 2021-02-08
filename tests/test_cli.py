from argparse import ArgumentParser
from sndslib import cli


def test_cli_has_a_parser():
    assert isinstance(cli.parser, ArgumentParser)


def test_cli_prog_name():
    assert cli.parser.prog == 'snds'


def test_cli_description():
    assert cli.parser.description == 'Searches and formats the SNDS dashboard data'
