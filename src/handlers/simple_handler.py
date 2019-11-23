import logging
import requests

from src.helpers.event_response import construct_response
from src.helpers.event_response import error_response

log = logging.getLogger()
log.setLevel(logging.INFO)


def hello_world(event, context):
    try:
        log.info(f'Hello World!')

        return construct_response(requests.codes.ok, 'Hello World')
    except:
        message = 'ERROR: Goodbye world!'
        return error_response(event, message, log)


def test_sns(event, context):
    try:
        log.info(f'Testing sns!')

        raise Exception('ERROR: TESTING SNS!')
    except:
        message = 'ERROR: TESTING SNS!'
        return error_response(event, message, log)
