# SNDS LIB

[![Build Status](https://www.travis-ci.com/undersfx/sndslib.svg?branch=master)](https://www.travis-ci.com/undersfx/sndslib) [![codecov](https://codecov.io/gh/undersfx/sndslib/branch/master/graph/badge.svg)](https://codecov.io/gh/undersfx/sndslib) [![Python 3](https://pyup.io/repos/github/undersfx/sndslib/python-3-shield.svg)](https://pyup.io/repos/github/undersfx/sndslib/) [![Updates](https://pyup.io/repos/github/undersfx/sndslib/shield.svg)](https://pyup.io/repos/github/undersfx/sndslib/) [![Total alerts](https://img.shields.io/lgtm/alerts/g/undersfx/sndslib.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/undersfx/sndslib/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/undersfx/sndslib.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/undersfx/sndslib/context:python)

Process and verify data from Microsoft's Smart Network Data Service (SNDS) API easily.

SNDSLIB is a wrapper around SNDS Automated Data Access API to facilitate fast data process and analysis.

---

## Table of content

- [What is SNDS?](#what-is-snds)
- [Installation](#installation)
- [CLI](#cli)
	- [Summary of all IPs status](#summary-of-all-ips-status)
	- [Individual report of a IP](#individual-report-of-a-ip)
	- [List all IPs blocked](#list-all-ips-blocked)
	- [List all IPs blocked with rDNS](#list-all-ips-blocked-with-rdns)
- [Incorporate SNDSLIB CLI](#incorporate-sndslib-cli)
- [More about SNDS](#more-about-snds)

---

## What is SNDS?

Smart Network Data Service (SNDS) is a platform to monitor data from IPs that send emails to Microsoft's servers.

If you send a substantial volume of email messages from your IPs, your can get valuable information about IP reputation, possible blocks, spam complaints and spamtraps hits.

First, you need to sign up for SNDS, [request access](https://sendersupport.olc.protection.outlook.com/snds/addnetwork.aspx) for your IPs, then enable the [Automates Data Access](https://sendersupport.olc.protection.outlook.com/snds/auto.aspx?wa=wsignin1.0) to recieve your API key.

---

## Installation

SNDSLIB has no external dependencies. It runs just with python 3.6 or higher.

```bash
pip install sndslib
```

Simple example of library usage:

```python
    >>> from sndslib import sndslib

    # Connects with snds to get usage data
    >>> r = sndslib.get_data('mykey')

    # Sndslib can give a summary of the state of all IPs
    >>> sndslib.summarize(r)
    {'red': 272, 'green': 710, 'yellow': 852, 'traps': 1298, 'ips': 1834, 'date': '12/31/2019'}

    # even get whole information about a specific IP
    >>> sndslib.search_ip_status('1.1.1.1', r)
    {'activity_end': '12/31/2019 7:00 PM',
    'activity_start': '12/31/2019 10:00 AM',
    'comments': '',
    'complaint_rate': '< 0.1%',
    'data_commands': '1894',
    'filter_result': 'GREEN',
    'ip_address': '1.1.1.1',
    'message_recipients': '1894',
    'rcpt_commands': '1895',
    'sample_helo': '',
    'sample_mailfrom': '',
    'trap_message_end': '',
    'trap_message_start': '',
    'traphits': '0'}

    # Connects with snds to get blocked ranges
    >>> r = sndslib.get_ip_status('mykey')

    # Sndslib can parse the information and extract all blocked IPs
    >>> blocked_ips = sndslib.list_blocked_ips(r)
    >>> print(blocked_ips)
    ['1.1.1.1', '1.1.1.2']

    # Even get all rdns for these IPs
    >>> sndslib.list_blocked_ips_rdns(blocked_ips)
    [{'ip': '1.1.1.1', 'rdns': 'foo.bar.exemple.com'},
     {'ip': '1.1.1.2', 'rdns': 'foo2.bar.exemple.com'}]
```

---

## CLI

This library contains a CLI to facilitate fast operations in the terminal. Here are some examples of their usage:

### Summary of all IPs status
```bash
snds -k 'your-key-here' -s
```
Example output:
```
Date: 12/31/2020
IPs:       1915
Green:      250
Yellow:    1175
Red:        490
Trap Hits:  990
Blocked:    193
```

### Individual report of a IP
```bash
snds -k 'your-key-here' -ip '1.1.1.1'
```

Example output:
```
Activity: 1/31/2020 11:59 AM until 1/31/2020 11:59 PM
IP:         1.1.1.1
Messages:    183057
Filter:       GREEN
Complaint:   < 0.1%
Trap Hits:        3
```

### List all IPs blocked
```bash
snds -k 'your-key-here' -l
```

Example output:
```
1.1.1.1
1.1.1.2
1.1.1.3
...
```

### List all IPs blocked with rDNS
```bash
snds -k 'your-key-here' -r
```

Example output:
```
1.1.1.1;example.domain1.com
1.1.1.2;example.domain2.com
1.1.1.3;example.domain3.com
...
```

---

## Incorporate SNDSLIB CLI

You can easily incorporate the sndslib CLI into your own command line tool by using the CLI adapter class:

```python
    from sndslib import cli

    # ... parse key, date and ip arguments

    # Create a instance of the Cli
    command = cli.Cli(key, date)

    # to implement -s flag use
    command.summary()

    # to implement -ips flag use
    command.ip_data(ip)

    # to implement -l flag use
    command.list_blocked_ips()

    # to implement -r flag use
    command.list_blocked_ips_rdns()
```

---

## More about SNDS

You can get more information about SNDS features in the Microsoft's official pages for [SNDS](https://sendersupport.olc.protection.outlook.com/snds/FAQ.aspx?wa=wsignin1.0) and [SNDS Automated Data Access](https://sendersupport.olc.protection.outlook.com/snds/auto.aspx).
