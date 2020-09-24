# SNDS LIB

Process and erify data from Microsoft's Smart Network Data Service (SNDS) API easily.

SNDSLIB is a wrapper around SNDS Automated Data Access API to facilitate fast data process and analysis.

## What is SNDS?

Smart Network Data Service (SNDS) is a platform to monitor data from IPs that send emails to Microsoft's servers. If you send more than 100 messages per day from your IPs, your can get valuable information about IP reputation, possible blocks, spam complaints and spamtraps hits.

## Talk is cheap. Show me the code!

Simple example of library use:

```python
    >>> from sndslib import sndslib

    >>> r = sndslib.get_ip_status('mykey')
    >>> blocked_ips = sndslib.list_blocked_ips(r)
    [1.1.1.1, 2.2.2.2, 3.3.3.3]

    >>> r = sndslib.get_data('mykey')
    >>> sndslib.summarize(r)
    {'red': 272, 'green': 710, 'yellow': 852, 'traps': 1298, 'ips': 1834, 'date': '12/31/2019'}

    >>> sndslib.search_ip_status('3.3.3.3', r)
    {'activity_end': '12/31/2019 7:00 PM',
    'activity_start': '12/31/2019 10:00 AM',
    'comments': '',
    'complaint_rate': '< 0.1%',
    'data_commands': '1894',
    'filter_result': 'GREEN',
    'ip_address': '3.3.3.3',
    'message_recipients': '1894',
    'rcpt_commands': '1895',
    'sample_helo': '',
    'sample_mailfrom': '',
    'trap_message_end': '',
    'trap_message_start': '',
    'traphits': '0'}
```

More information in the [SNDS](https://sendersupport.olc.protection.outlook.com/snds/FAQ.aspx?wa=wsignin1.0) and [SNDS Automated Data Access](https://sendersupport.olc.protection.outlook.com/snds/auto.aspx) pages.
