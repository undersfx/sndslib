from sndslib import cli
import sys


def test_cli_data_exit_on_bad_request(capsys):
    sys.argv = ['cli.py', '-k', 'test', '-s', '-d', '000000']
    try:
        cli.main()
    except SystemExit:
        pass
    else:
        raise AssertionError
