# cloud-tasks-deferred-v2

A deferred library for Google Cloud Tasks.

Fork of [python-cloud-tasks-deferred](https://github.com/grktsh/python-cloud-tasks-deferred) originally created by [Atsushi Hanaoka](https://github.com/grktsh).

## Key differences

- Migrated to google-cloud-tasks 2.0.0
- Dropped Python 2 support
- Added Flask integration

## Installation

Addd following handler to your app.yaml

```yaml
- url: /_tasks/deferred
  script: cloud_tasks_deferred.wsgi.application
  login: admin
```

Initialize module in flask
```python
from cloud_tasks_deferred_v2.flask import init_deferred

init_deferred(app)
```


## Prerequisites

-   Environment variable `QUEUE_LOCATION` in which Cloud Tasks service runs

## Unavailable options

-   `_transactional`: Transactional tasks are unavailable in Cloud Tasks
-   `_retry_options`: Retry options for tasks are unavailable in Cloud
    Tasks

## Unimplemented features
  
- Support for tasks larger than 10 KB
