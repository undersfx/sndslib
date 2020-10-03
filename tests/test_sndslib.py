from sndslib import __version__
from sndslib import sndslib
import pytest


def test_version():
    assert __version__ == '0.1.1'


def test_get_ip_status_fail_without_key():
    with pytest.raises(TypeError):
        sndslib.get_ip_status()


def test_get_ip_status_is_list(get_ip_status_mock):
    resp = sndslib.get_ip_status('test')
    assert isinstance(resp, list)


def test_get_ip_status_have_ips(get_ip_status_mock):
    resp = sndslib.get_ip_status('test')
    assert '1.1.1.0' in resp[0]


def test_get_ip_status_first_list_value(get_ip_status_mock):
    resp = sndslib.get_ip_status('test')
    first_line_resp = '1.1.1.0,1.1.1.1,Yes,Blocked due to user complaints or other evidence of spamming'
    assert first_line_resp == resp[0]


def test_get_ip_status_len(get_ip_status_mock):
    resp = sndslib.get_ip_status('test')
    assert len(resp) == 3


def test_get_data_fail_without_key():
    with pytest.raises(TypeError):
        sndslib.get_data()


def test_get_data_is_list(get_data_mock):
    resp = sndslib.get_data('test')
    assert isinstance(resp, list)


def test_get_data_have_ips(get_data_mock):
    resp = sndslib.get_data('test')
    assert '1.1.1.0' in resp[0]


def test_get_data_first_value(get_data_mock):
    resp = sndslib.get_data('test')
    first_line_value = '1.1.1.0,12/31/2019 8:00 AM,9/29/2020 9:00 PM,14129,14129,13025,GREEN,< 0.1%,9/29/2020 8:07 AM,9/29/2020 12:03 PM,41,,,'  # noqa
    assert first_line_value == resp[0]


def test_get_data_len(get_data_mock):
    resp = sndslib.get_data('test')
    assert len(resp) == 3


def test_summarize_return_dict(get_data_mock):
    resp = sndslib.get_data('test')
    summary = sndslib.summarize(resp)
    assert isinstance(summary, dict)


def test_summarize_green_count(get_data_mock):
    resp = sndslib.get_data('test')
    summary = sndslib.summarize(resp)
    assert summary['green'] == 1


def test_summarize_yellow_count(get_data_mock):
    resp = sndslib.get_data('test')
    summary = sndslib.summarize(resp)
    assert summary['yellow'] == 1


def test_summarize_red_count(get_data_mock):
    resp = sndslib.get_data('test')
    summary = sndslib.summarize(resp)
    assert summary['red'] == 1
