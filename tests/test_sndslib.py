from sndslib import __version__
from sndslib import sndslib
import pytest


def test_version():
    assert __version__ == '0.1.2'


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


def test_get_data_with_date_is_list(get_data_mock):
    resp = sndslib.get_data('test', '290920')
    assert isinstance(resp, list)


def test_get_data_have_ips(get_data_mock):
    resp = sndslib.get_data('test')
    assert '1.1.1.0' in resp[0]


def test_get_data__with_date_have_ips(get_data_mock):
    resp = sndslib.get_data('test', '290920')
    assert '1.1.1.0' in resp[0]


def test_get_data_first_value(get_data_mock):
    resp = sndslib.get_data('test')
    first_line_value = '1.1.1.0,12/31/2019 8:00 AM,9/29/2020 9:00 PM,14129,14129,13025,GREEN,< 0.1%,9/29/2020 8:07 AM,9/29/2020 12:03 PM,41,,,'  # noqa
    assert first_line_value == resp[0]


def test_get_data__with_date_first_value(get_data_mock):
    resp = sndslib.get_data('test', '290920')
    first_line_value = '1.1.1.0,12/31/2019 8:00 AM,9/29/2020 9:00 PM,14129,14129,13025,GREEN,< 0.1%,9/29/2020 8:07 AM,9/29/2020 12:03 PM,41,,,'  # noqa
    assert first_line_value == resp[0]


def test_get_data_len(get_data_mock):
    resp = sndslib.get_data('test')
    assert len(resp) == 3


def test_get_data_with_date_len(get_data_mock):
    resp = sndslib.get_data('test', '290920')
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


def test_search_ip_status_return_success(get_data_mock):
    resp = sndslib.get_data('test')
    resp_dict = sndslib.search_ip_status('1.1.1.0', resp)
    expected_return = {
        'ip_address': '1.1.1.0',
        'activity_start': '12/31/2019 8:00 AM',
        'activity_end': '9/29/2020 9:00 PM',
        'rcpt_commands': '14129',
        'data_commands': '14129',
        'message_recipients': '13025',
        'filter_result': 'GREEN',
        'complaint_rate': '< 0.1%',
        'trap_message_start': '9/29/2020 8:07 AM',
        'trap_message_end': '9/29/2020 12:03 PM',
        'traphits': '41', 'sample_helo': '',
        'sample_mailfrom': '',
        'comments': ''
        }
    assert resp_dict == expected_return


def test_search_ip_status_return_failure(get_data_mock):
    resp = sndslib.get_data('test')
    resp_dict = sndslib.search_ip_status('0.0.0.0', resp)
    assert bool(resp_dict) is False


def test_search_ip_status_return_failure_type(get_data_mock):
    resp = sndslib.get_data('test')
    resp_dict = sndslib.search_ip_status('0.0.0.0', resp)
    assert isinstance(resp_dict, dict)


def test_list_blocked_ips_success_type(get_ip_status_mock):
    resp = sndslib.get_ip_status('test')
    resp_list = sndslib.list_blocked_ips(resp)
    assert isinstance(resp_list, list)


def test_list_blocked_ips_success_value(get_ip_status_mock):
    resp = sndslib.get_ip_status('test')
    blocked_ips = sndslib.list_blocked_ips(resp)
    assert blocked_ips == ['1.1.1.0', '1.1.1.1', '1.1.1.3', '1.1.1.254', '1.1.1.255', '1.1.2.0', '1.1.2.1']


def test_list_blocked_ips_rdns_success(get_ip_status_mock, socket_mock):
    resp = sndslib.get_ip_status('test')
    blocked_ips = sndslib.list_blocked_ips(resp)
    rdns_return = sndslib.list_blocked_ips_rdns(blocked_ips)
    expected_return = [
        {'ip': '1.1.1.0', 'rdns': 'rnds.mock.com'},
        {'ip': '1.1.1.1', 'rdns': 'rnds.mock.com'},
        {'ip': '1.1.1.3', 'rdns': 'rnds.mock.com'},
        {'ip': '1.1.1.254', 'rdns': 'rnds.mock.com'},
        {'ip': '1.1.1.255', 'rdns': 'rnds.mock.com'},
        {'ip': '1.1.2.0', 'rdns': 'rnds.mock.com'},
        {'ip': '1.1.2.1', 'rdns': 'rnds.mock.com'}
        ]
    assert rdns_return == expected_return


def test_list_blocked_ips_rdns_failure(get_ip_status_mock):
    rdns_return = sndslib.list_blocked_ips_rdns(['0.0.0.1', '0.0.0.1'])
    expected_return = [
        {'ip': '0.0.0.1', 'rdns': 'NXDOMAIN'},
        {'ip': '0.0.0.1', 'rdns': 'NXDOMAIN'}
        ]
    assert rdns_return == expected_return


def test_list_blocked_ips_rdns_success_single_ip(get_ip_status_mock, socket_mock):
    rdns_return = sndslib.list_blocked_ips_rdns('1.1.1.0')
    expected_return = [{'ip': '1.1.1.0', 'rdns': 'rnds.mock.com'}]
    assert rdns_return == expected_return


def test_list_blocked_ips_rdns_failure_single_ip(get_ip_status_mock):
    rdns_return = sndslib.list_blocked_ips_rdns('0.0.0.1')
    assert rdns_return == [{'ip': '0.0.0.1', 'rdns': 'NXDOMAIN'}]


def test_list_blocked_ips_rdns_empty_list(get_ip_status_mock):
    rdns_return = sndslib.list_blocked_ips_rdns([])
    assert rdns_return == []
