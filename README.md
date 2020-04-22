Supervisor-logging
==================

A [supervisor] plugin to stream events to an external Syslog instance (for
example, Logstash).

Installation
------------

Python 2.7 or Python 3.2+ is required.

```
pip install supervisor-logging
```

Note that supervisor itself does not yet work on Python 3, though it can be
installed in a separate environment (because supervisor-logging is a separate
process).

Usage
-----

The Syslog instance to send the events to is configured with the environment
variables:

* `SYSLOG_SERVER`
* `SYSLOG_PORT`
* `SYSLOG_PROTO`
* `SYSLOG_FACILITY`

Add the plugin as an event listener in your `supervisord.conf` file:

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
