import logging
import requests
import base64
import json

from src.helpers.event_response import construct_response
from src.helpers.event_response import error_response

log = logging.getLogger()
log.setLevel(logging.INFO)


def demo_kinesis_event(event, context):
    try:
        log.info(f'Event triggered from kinesis')
        data = base64.b64decode(event['Records'][0]['kinesis']['data']).decode("utf-8")

        if 'email' in data:
            payload = {
                'name': 'ALERT',
                'email': 'arjun@example.com',
                'content': data
            }
            log.info(f'Sending email with {payload}')
            headers = {'Content-Type': 'application/json'}
            requests.post(url='https://st-dev.cb-learning.com/api/v1/email/send',
                          data=json.dumps(payload),
                          headers=headers)
        else:
            log.info(data)

        return construct_response(requests.codes.ok, f'Triggered kinesis event')
    except:
        log.info(f'Something bad happened for {event}')
        message = 'ERROR: Goodbye world!'
        return error_response(event, message, log)
