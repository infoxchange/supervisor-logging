#!/bin/sh -e
# Install supervisord into Python 2.7 environment, regardless of the one
# currently active, and make it available in PATH.

. ~/virtualenv/python2.7/bin/activate

pip install supervisor

if [ "$SUPERVISOR_PYTHON_VERSION" != "$TRAVIS_PYTHON_VERSION" ]
then
    ln -s ~/virtualenv/python$SUPERVISOR_PYTHON_VERSION/bin/supervisorctl \
    ln -s ~/virtualenv/python$SUPERVISOR_PYTHON_VERSION/bin/supervisord \
        ~/virtualenv/python$TRAVIS_PYTHON_VERSION/bin
fi

deactivate
