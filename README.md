Supervisor-logging
==================

A [supervisor] plugin to stream events to an external Syslog instance (for
example, Logstash).

Installation
------------

```
pip install supervisor-logging
```

Usage
-----

The Syslog instance to send the events to is configured with the environment
variables:

* `SYSLOG_SERVER`
* `SYSLOG_PORT`
* `SYSLOG_PROTO`

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
