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
Test supervisor_logging.
"""

import os
import re
import socket
import SocketServer as socketserver
import subprocess
import threading

from time import sleep

from unittest import TestCase


def strip_volatile(message):
    """
    Strip volatile parts (PID, datetime) from a logging message.
    """

    volatile = (
        (socket.gethostname(), 'HOST'),
        (r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z', 'DATE'),
    )

    for regexp, replacement in volatile:
        message = re.sub(regexp, replacement, message)

    return message


class SupervisorLoggingTestCase(TestCase):
    """
    Test logging.
    """

    maxDiff = None

    def test_logging(self):
        """
        Test logging.
        """

        print "Disabled."
        return True

        messages = []

        class GraylogHandler(socketserver.BaseRequestHandler):
            """
            Save received messages.
            """

            def handle(self):
                messages.append(self.request[0].strip().decode())

        graylog = socketserver.UDPServer(('0.0.0.0', 0), GraylogHandler)
        try:
            threading.Thread(target=graylog.serve_forever).start()

            env = os.environ.copy()
            env['GRAYLOG_SERVER'] = "127.0.0.1"
            env['GRAYLOG_PORT'] = str(graylog.server_address[1])

            mydir = os.path.dirname(__file__)

            supervisor = subprocess.Popen(
                ['supervisord', '-c', os.path.join(mydir, 'supervisord.conf')],
                env=env,
            )
            try:

                sleep(3)

                pid = subprocess.check_output(
                    ['supervisorctl', 'pid', 'messages']
                ).strip()

                sleep(8)

                self.assertEqual(
                    list(map(strip_volatile, messages)),
                    ['<14>DATE HOST messages[{pid}]: Test {i} \n\x00'.format(
                        pid=pid,
                        i=i)
                     for i in range(4)]
                )
            finally:
                supervisor.terminate()

        finally:
            graylog.shutdown()
