import logging

from cloud_tasks_deferred_v2 import deferred

logger = logging.getLogger(__name__)


def application(environ: dict, start_response):
    """A WSGI application that processes deferred invocations."""

    def abort(status):
        start_response(status, [('Content-Type', 'text/plain')])
        return []

    if environ['REQUEST_METHOD'] != 'POST':
        return abort('405 Method Not Allowed')

    if environ.get('CONTENT_TYPE') != 'application/octet-stream':
        return abort('415 Unsupported Media Type')

    if not any(key.upper() == 'HTTP_X_APPENGINE_TASKNAME' for key in environ):
        logger.error(
            'Detected an attempted XSRF attack. '
            'The header "X-AppEngine-Taskname" was not set.'
        )
        return abort('403 Forbidden')

    headers = [
        k + ':' + v
        for k, v in environ.items()
        if k.upper().startswith('HTTP_X_APPENGINE_')
    ]
    # noinspection PyProtectedMember
    logger.log(deferred._DEFAULT_LOG_LEVEL, ', '.join(headers))

    content_length = int(environ.get('CONTENT_LENGTH', 0))
    data = environ['wsgi.input'].read(content_length)

    # noinspection PyBroadException
    try:
        deferred.run(data)
    except deferred.SingularTaskFailure:
        logger.debug('Failure executing task, task retry forced')
        return abort('408 Request Timeout')
    except deferred.PermanentTaskFailure:
        logger.exception('Permanent failure attempting to execute task')
    except Exception:
        return abort('500 Internal Server Error')

    start_response('204 No Content', [])
    return []
