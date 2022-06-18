from sndslib import cli, sndslib, __version__
from argparse import ArgumentParser
import sys

from sndslib.utils import Presenter


def test_cli_has_a_parser():
    assert isinstance(cli.parser, ArgumentParser)


def test_cli_prog_name():
    assert cli.parser.prog == 'snds'


def test_cli_description():
    assert cli.parser.description == 'Searches and formats the SNDS dashboard data'


def test_print_list_blocked_ips(capsys, blocked_ips_mock):
    presenter = Presenter()
    presenter.list_blocked_ips(blocked_ips_mock)
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


def test_print_list_blocked_ips_rdns(capsys, blocked_ips_rdns_mock):
    presenter = Presenter()
    presenter.list_blocked_ips_rdns(blocked_ips_rdns_mock)
    captured = capsys.readouterr()
    expected_return = [
        '1.1.1.0;rdns.mock.com',
        '1.1.1.1;rdns.mock.com',
        '1.1.1.3;rdns.mock.com',
        '1.1.1.254;rdns.mock.com',
        '1.1.1.255;rdns.mock.com',
        '1.1.2.0;rdns.mock.com',
        '1.1.2.1;rdns.mock.com',
        '1.1.255.255;rdns.mock.com',
        '1.2.0.0;rdns.mock.com',
        '1.255.255.255;rdns.mock.com',
        '2.0.0.0;rdns.mock.com',
    ]
    for s in expected_return:
        assert s in captured.out


def test_print_summary_data_mock(capsys, get_data_urlopen_mock):
    presenter = Presenter()
    resp = sndslib.get_data('test')
    summary = sndslib.summarize(resp)
    presenter.summary(summary, ['1.1.1.1'])
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
    presenter = Presenter()
    presenter.summary(summary, blocked_ips_mock)
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
    command = cli.Cli('test')
    presenter = Presenter()
    ipdata = sndslib.search_ip_status('1.1.1.2', command.usage_data)
    presenter.ip_data(ipdata)
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


def test_main_summarize(capsys, get_data_function_mock, get_ip_status_function_mock):
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


def test_main_summarize_with_date(capsys, get_data_function_mock, get_ip_status_function_mock):
    sys.argv = ['cli.py', '-k', 'test', '-s', '-d', '092920']
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


def test_main_list_blocked(capsys, get_data_function_mock, get_ip_status_function_mock):
    sys.argv = ['cli.py', '-k', 'test', '-l']
    cli.main()
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


def test_main_list_ip_data_success(capsys, get_data_function_mock, get_ip_status_function_mock):
    sys.argv = ['cli.py', '-k', 'test', '-ip', '1.1.1.2']
    cli.main()
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


def test_main_list_ip_data_failure(capsys, get_data_function_mock, get_ip_status_function_mock):
    sys.argv = ['cli.py', '-k', 'test', '-ip', '2.0.0.0']
    cli.main()
    captured = capsys.readouterr()
    assert 'No data found for the given IP.\n' in captured.out


def test_main_list_blocked_rdns_success(capsys, get_data_function_mock, get_ip_status_function_mock, socket_mock):
    sys.argv = ['cli.py', '-k', 'test', '-r']
    cli.main()
    captured = capsys.readouterr()
    expected_return = [
        '1.1.1.0;rdns.mock.com',
        '1.1.1.1;rdns.mock.com',
        '1.1.1.3;rdns.mock.com',
        '1.1.1.254;rdns.mock.com',
        '1.1.1.255;rdns.mock.com',
        '1.1.2.0;rdns.mock.com',
        '1.1.2.1;rdns.mock.com',
        '1.1.255.255;rdns.mock.com',
        '1.2.0.0;rdns.mock.com',
        '1.255.255.255;rdns.mock.com',
        '2.0.0.0;rdns.mock.com',
        ]
    for s in expected_return:
        assert s in captured.out


def test_main_list_blocked_rdns_failure(capsys, get_data_function_mock, get_ip_status_function_mock, socket_error_mock):
    sys.argv = ['cli.py', '-k', 'test', '-r']
    cli.main()
    captured = capsys.readouterr()
    expected_return = [
        '1.1.1.0;NXDOMAIN',
        '1.1.1.1;NXDOMAIN',
        '1.1.1.3;NXDOMAIN',
        '1.1.1.254;NXDOMAIN',
        '1.1.1.255;NXDOMAIN',
        '1.1.2.0;NXDOMAIN',
        '1.1.2.1;NXDOMAIN',
        '1.1.255.255;NXDOMAIN',
        '1.2.0.0;NXDOMAIN',
        '1.255.255.255;NXDOMAIN',
        '2.0.0.0;NXDOMAIN',
        ]
    for s in expected_return:
        assert s in captured.out


def test_main_version(capsys):
    sys.argv = ['cli.py', '-V']
    try:
        cli.main()
    except SystemExit:
        pass
    finally:
        captured = capsys.readouterr()
    assert f'sndslib {__version__}' in captured.out


def test_cli_class_instance():
    key = 'test'
    test_cli = cli.Cli(key)
    assert test_cli.key == key


def test_cli_ip_status_exit_on_bad_request(capsys, urlopen_raises_httperror_mock):
    sys.argv = ['cli.py', '-k', 'test', '-l']
    try:
        cli.main()
    except SystemExit:
        pass
    else:
        raise AssertionError
