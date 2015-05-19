Supervisor-logging
==================

A [supervisor] plugin to stream events to an external Graylog instance.

Installation
------------

```
git clone https://github.com/peterfroehlich/supervisor-logging.git
cd supervisor-logging
python setup.py install
```

Usage
-----

The Graylog server to send the events to is configured with the environment
variables:

* `GRAYLOG_SERVER`
* `GRAYLOG_PORT`

Add the plugin as an event listener:

```
[eventlistener:logging]
command = supervisor_logging
events = PROCESS_LOG
```

Enable the log events in your program:

```
[program:yourprogram]
stdout_events_enabled = true
stderr_events_enabled = true
```

[supervisor]: http://supervisord.org/
