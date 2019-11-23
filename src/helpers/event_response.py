import json
import traceback
import requests

from src.helpers.serializers import DecimalEncoder
from src.sns.sns_handler import drop_into_sns


def construct_response(status_code, body):
    response = {
        "statusCode": status_code,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps(body, cls=DecimalEncoder)
    }

    return response


def error_response(event, message, log):
    log.error(traceback.format_exc())
    log.error(message)
    drop_into_sns(message)
    return construct_response(requests.codes.internal_server_error, message)
