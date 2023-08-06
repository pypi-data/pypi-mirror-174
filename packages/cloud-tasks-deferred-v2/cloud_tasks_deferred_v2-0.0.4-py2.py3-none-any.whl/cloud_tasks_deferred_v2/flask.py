import logging

from flask import Blueprint, Flask
from flask import request

from cloud_tasks_deferred_v2 import deferred

app = Blueprint('cloud_tasks_deferred', __name__)
logger = logging.getLogger(__name__)


@app.route('/_tasks/deferred', methods=['POST'])
def task_runner():
    if request.content_type != 'application/octet-stream':
        return '', '415 Unsupported Media Type'

    deferred.run(request.get_data())
    return '', '204 No Content'


def init_deferred(application: Flask):
    application.register_blueprint(app)
