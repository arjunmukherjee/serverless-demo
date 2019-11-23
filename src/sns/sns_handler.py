import logging
import boto3

from src.helpers.environment_helper import get_sns_arn
from src.helpers.environment_helper import get_slack_webhook
from src.helpers.event_response import *

log = logging.getLogger()
log.setLevel(logging.DEBUG)

sns_client = None


def error_handler(event, context):
    try:
        message = event['Records'][0]['Sns']['Message']

        log.info(f'Posting {message} to slack')
        __post_to_slack(str(message))
    except:
        log.error('Problem processing error message')

    return construct_response(requests.codes.ok, 'Processed the poison pill')


def drop_into_sns(message):
    global sns_client
    if not sns_client:
        sns_client = boto3.client('sns')

    response = sns_client.publish(
        TargetArn=get_sns_arn(),
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )

    return response


def __post_to_slack(message):
    channel = '#test-sls-webhook'
    url = f'https://hooks.slack.com/services/T02Q6DY7G/{get_slack_webhook()}'
    text = f"BAD STUFF HAPPENED [{message}]"
    data = '{ "channel": "' + channel + '", "color": "#FF0000", ' \
                                        '"attachments": [ { "color": "#FF0000", "text": "' + text + '" } ] }'

    requests.post(url, data=data)
