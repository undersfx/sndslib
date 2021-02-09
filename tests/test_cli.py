from argparse import ArgumentParser
from sndslib import cli, sndslib


def test_cli_has_a_parser():
    assert isinstance(cli.parser, ArgumentParser)


def test_cli_prog_name():
    assert cli.parser.prog == 'snds'


def test_cli_description():
    assert cli.parser.description == 'Searches and formats the SNDS dashboard data'


def test_format_list_blocked_ips(capsys, blocked_ips_mock):
    cli.format_list_blocked_ips(blocked_ips_mock)
    captured = capsys.readouterr()
    assert '2.0.0.0' in captured.out


def test_format_list_blocked_ips_rdns(capsys, blocked_ips_rdns_mock):
    cli.format_list_blocked_ips_rdns(blocked_ips_rdns_mock)
    captured = capsys.readouterr()
    assert 'rnds.mock.com' in captured.out


def test_format_ip_status_data_mock(capsys, get_data_mock):
    resp = sndslib.get_data('test')
    summary = sndslib.summarize(resp)
    cli.format_ip_status(summary, ['1.1.1.1'])
    captured = capsys.readouterr()
    print(captured.out)
    assert 'IPs:          3' in captured.out


def test_format_ip_status_blocked_ips_mock(capsys, blocked_ips_mock):
    summary = {
        'date': '09/29/2020', 'green': 1,
        'ips': 3, 'red': 1, 'traps': 107,
        'yellow': 1
        }
    cli.format_ip_status(summary, blocked_ips_mock)
    captured = capsys.readouterr()
    assert 'Blocked:     11' in captured.out
