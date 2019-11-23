import logging
import requests
import time

from urllib.parse import unquote

from src.helpers.event_response import construct_response
from src.helpers.event_response import error_response
from src.dynamo.dynamo_methods import dynamo_save_item
from src.dynamo.dynamo_methods import dynamo_lookup_item
from src.kinesis.kinesis_methods import kinesis_put_item


log = logging.getLogger()
log.setLevel(logging.INFO)


def demo_dynamo_save(event, context):
    try:
        keyword = __extract_parameter(event, 'keyword')
        data = __extract_parameter(event, 'data')
        expire_at = int(time.time() + 30)
        log.info(f'Lets persist this {keyword}:{data}:{expire_at} into dynamo')

        some_random_object = {
            'keyword': keyword,
            'expireAt': expire_at,
            'value': data
        }
        __save_time(some_random_object)

        return construct_response(requests.codes.ok, f'{keyword} persisted in dynamo')
    except:
        message = 'ERROR: Could not execute save!'
        return error_response(event, message, log)


def __save_time(item):
    dynamo_save_item(item)
    kinesis_put_item(item)


def demo_dynamo_find(event, context):
    try:
        keyword = __extract_parameter(event, 'keyword')
        log.info(f'Lets look for this {keyword} in dynamo')

        item = dynamo_lookup_item(keyword)
        if not item:
            log.info(f'No items found for keyword {keyword} in dynamo')
            return construct_response(requests.codes.ok, f'No items found for keyword {keyword} in dynamo')

        return construct_response(requests.codes.ok, f'{item}')
    except:
        message = 'ERROR: Could not execute find!'
        return error_response(event, message, log)


def demo_dynamo_event(event, context):
    try:
        log.info(f'Event triggered from dynamo')

        for item in event['Records']:
            event_type = item['eventName']
            if event_type == 'REMOVE':
                image_name = 'OldImage'
            else:
                image_name = 'NewImage'

            record = item['dynamodb'][image_name]
            log.info(f'{event_type} {record} from dynamo')

        return construct_response(requests.codes.ok, f'Triggered event')
    except:
        log.info(f'Something bad happened for {event}')
        message = 'ERROR: Goodbye world!'
        return error_response(event, message, log)


def __extract_parameter(event, parameter):
    param_value = unquote(event['pathParameters'].get(parameter))
    return param_value
