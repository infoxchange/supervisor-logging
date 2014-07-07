#!/usr/bin/env python
#
# Copyright 2014  Infoxchange Australia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Send received events to a syslog instance.
"""

from __future__ import print_function

import logging
import logging.handlers
import os
import re
import socket
import sys


class PalletFormatter(logging.Formatter):
    """
    A formatter for the Pallet environment.
    """

    HOSTNAME = re.sub(
        r':\d+$', '', os.environ.get('SITE_DOMAIN', socket.gethostname()))
    FORMAT = '%(asctime)s {hostname} %(name)s[%(process)d]: %(message)s'.\
        format(hostname=HOSTNAME)
    DATE_FORMAT = '%b %d %H:%M:%S'

    def __init__(self):
        super(PalletFormatter, self).__init__(fmt=self.FORMAT,
                                              datefmt=self.DATE_FORMAT)

    def format(self, record):
        # strip newlines
        message = super(PalletFormatter, self).format(record)
        message = message.replace('\n', ' ')
        message += '\n'
        return message


class SysLogHandler(logging.handlers.SysLogHandler):
    """
    A SysLogHandler not appending NUL character to messages
    """
    append_nul = False


def get_headers(line):
    """
    Parse Supervisor message headers.
    """

    return dict([x.split(':') for x in line.split()])


def eventdata(payload):
    """
    Parse a Supervisor event.
    """

    headerinfo, data = payload.split('\n', 1)
    headers = get_headers(headerinfo)
    return headers, data


def supervisor_events(stdin, stdout):
    """
    An event stream from Supervisor.
    """

    while True:
        stdout.write('READY\n')
        stdout.flush()

        line = stdin.readline()
        headers = get_headers(line)

        payload = stdin.read(int(headers['len']))
        event_headers, event_data = eventdata(payload)

        yield event_headers, event_data

        stdout.write('RESULT 2\nOK')
        stdout.flush()


def main():
    """
    Main application loop.
    """

    env = os.environ

    try:
        host = env['SYSLOG_SERVER']
        port = int(env['SYSLOG_PORT'])
        socktype = socket.SOCK_DGRAM if env['SYSLOG_PROTO'] == 'udp' \
            else socket.SOCK_STREAM
    except KeyError:
        sys.exit("SYSLOG_SERVER, SYSLOG_PORT and SYSLOG_PROTO are required.")

    handler = SysLogHandler(
        address=(host, port),
        socktype=socktype,
    )
    handler.setFormatter(PalletFormatter())

    for event_headers, event_data in supervisor_events(sys.stdin, sys.stdout):
        event = logging.LogRecord(
            name=event_headers['processname'],
            level=logging.INFO,
            pathname=None,
            lineno=0,
            msg=event_data,
            args=(),
            exc_info=None,
        )
        event.process = int(event_headers['pid'])
        handler.handle(event)


if __name__ == '__main__':
    main()
