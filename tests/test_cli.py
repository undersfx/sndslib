from sndslib import cli, sndslib

from argparse import ArgumentParser
import sys


def test_cli_has_a_parser():
    assert isinstance(cli.parser, ArgumentParser)


def test_cli_prog_name():
    assert cli.parser.prog == 'snds'


def test_cli_description():
    assert cli.parser.description == 'Searches and formats the SNDS dashboard data'


def test_format_list_blocked_ips(capsys, blocked_ips_mock):
    cli.format_list_blocked_ips(blocked_ips_mock)
    captured = capsys.readouterr()
    expected_return = [
        '1.1.1.0',
        '1.1.1.1',
        '1.1.1.3',
        '1.1.1.254',
        '1.1.1.255',
        '1.1.2.0',
        '1.1.2.1',
        '1.1.255.255',
        '1.2.0.0',
        '1.255.255.255',
        '2.0.0.0',
    ]
    for s in expected_return:
        assert s in captured.out


def test_format_list_blocked_ips_rdns(capsys, blocked_ips_rdns_mock):
    cli.format_list_blocked_ips_rdns(blocked_ips_rdns_mock)
    captured = capsys.readouterr()
    expected_return = [
        '1.1.1.0;rnds.mock.com',
        '1.1.1.1;rnds.mock.com',
        '1.1.1.3;rnds.mock.com',
        '1.1.1.254;rnds.mock.com',
        '1.1.1.255;rnds.mock.com',
        '1.1.2.0;rnds.mock.com',
        '1.1.2.1;rnds.mock.com',
        '1.1.255.255;rnds.mock.com',
        '1.2.0.0;rnds.mock.com',
        '1.255.255.255;rnds.mock.com',
        '2.0.0.0;rnds.mock.com',
    ]
    for s in expected_return:
        assert s in captured.out


def test_format_ip_status_data_mock(capsys, get_data_urlopen_mock):
    resp = sndslib.get_data('test')
    summary = sndslib.summarize(resp)
    cli.format_ip_status(summary, ['1.1.1.1'])
    captured = capsys.readouterr()
    expected_return = [
        'Date: 09/29/2020 ',
        'IPs:          3 ',
        'Green:        1 ',
        'Yellow:       1 ',
        'Red:          1 ',
        'Trap Hits:  107 ',
        'Blocked:      1',
    ]
    for s in expected_return:
        assert s in captured.out


def test_format_ip_status_blocked_ips_mock(capsys, blocked_ips_mock):
    summary = {
        'date': '09/29/2020', 'green': 1,
        'ips': 3, 'red': 1, 'traps': 107,
        'yellow': 1
        }
    cli.format_ip_status(summary, blocked_ips_mock)
    captured = capsys.readouterr()
    expected_return = [
        'Date: 09/29/2020 ',
        'IPs:          3 ',
        'Green:        1 ',
        'Yellow:       1 ',
        'Red:          1 ',
        'Trap Hits:  107 ',
        'Blocked:     11',
    ]
    for s in expected_return:
        assert s in captured.out


def test_format_ip_data(capsys, get_data_urlopen_mock):
    rdata = sndslib.get_data('test')
    ipdata = sndslib.search_ip_status('1.1.1.2', rdata)
    cli.format_ip_data(ipdata)
    captured = capsys.readouterr()
    expected_return = [
        'Activity: 12/31/2019 9:00 PM until 9/29/2020 9:00 PM ',
        'IP:         1.1.1.2 ',
        'Messages:     12960 ',
        'Filter:         RED ',
        'Complaint:   < 0.1% ',
        'Trap Hits:       26 ',
        ]
    for s in expected_return:
        assert s in captured.out


def test_main(capsys, get_data_function_mock, get_ip_status_function_mock):
    sys.argv = ['cli.py', '-k', 'test', '-s']
    cli.main()
    captured = capsys.readouterr()
    expected_return = [
        'Date: 09/29/2020 ',
        'IPs:          3 ',
        'Green:        1 ',
        'Yellow:       1 ',
        'Red:          1 ',
        'Trap Hits:  107 ',
        'Blocked:     11',
        ]
    for s in expected_return:
        assert s in captured.out
