import pytest
from unittest.mock import Mock


IP_STATUS_VALUE = b"""1.1.1.0,1.1.1.1,Yes,Blocked due to user complaints or other evidence of spamming\r
1.1.1.3,1.1.1.3,Yes,Blocked due to user complaints or other evidence of spamming\r
1.1.1.254,1.1.2.1,Yes,Blocked due to user complaints or other evidence of spamming"""  # noqa

DATA_VALUE = b"""1.1.1.0,12/31/2019 8:00 AM,9/29/2020 9:00 PM,14129,14129,13025,GREEN,< 0.1%,9/29/2020 8:07 AM,9/29/2020 12:03 PM,41,,,\r
1.1.1.1,12/31/2019 9:00 PM,9/29/2020 9:00 PM,47386,47386,47384,YELLOW,< 0.1%,9/28/2020 9:08 PM,9/29/2020 8:09 PM,40,,,\r
1.1.1.2,12/31/2019 9:00 PM,9/29/2020 9:00 PM,14121,14121,12960,RED,< 0.1%,9/29/2020 8:07 AM,9/29/2020 11:53 AM,26,,,"""  # noqa


@pytest.fixture
def get_ip_status_mock(mocker):
    resp_mock = Mock()
    resp_mock.status = 200
    resp_mock.read.return_value = IP_STATUS_VALUE

    mock = mocker.patch('sndslib.sndslib.urlopen')
    mock.return_value = resp_mock
    return mock


@pytest.fixture
def get_data_mock(mocker):
    resp_mock = Mock()
    resp_mock.status = 200
    resp_mock.read.return_value = DATA_VALUE

    mock = mocker.patch('sndslib.sndslib.urlopen')
    mock.return_value = resp_mock
    return mock


@pytest.fixture
def socket_mock(mocker):
    mock = mocker.patch('sndslib.sndslib.socket.gethostbyaddr')
    mock.return_value = ('rnds.mock.com', '', '')
    return mock
