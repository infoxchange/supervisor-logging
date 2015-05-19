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
Setup script.
"""

from sys import exit, version_info
from setuptools import setup, find_packages

if not version_info[0] == 2 or not version_info[1] >= 6:
    print "Python 2.7 or higher required (and no python 3, sorry)"
    exit(1)

try:
    requirements = open('requirements.txt')
    test_requirements = open('test_requirements.txt')
    setup(
        name='supervisor-logging',
        version='0.0.8',
        description='Stream supervisord logs to a syslog instance',
        author='Infoxchange development team',
        author_email='devs@infoxchange.net.au',
        url='https://github.com/infoxchange/supervisor-logging',
        license='Apache 2.0',
        long_description=open('README.md').read(),

        packages=find_packages(exclude=['tests']),
        package_data={
            'forklift': [
                'README.md',
                'requirements.txt',
                'test_requirements.txt',
                "setup.py"
                'README.md',
                'requirements.txt',
                'test_requirements.txt',
                ],
            },
        entry_points={
            'console_scripts': [
                'supervisor_logging = supervisor_logging:main',
                ],
            },

        install_requires=requirements.read().splitlines(),

        test_suite='tests',
        tests_require=test_requirements.read().splitlines(),
        )
finally:
    requirements.close()
    test_requirements.close()
