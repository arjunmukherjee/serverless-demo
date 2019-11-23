import boto3
import logging

from src.dynamo.dynamo_helper import get_st_table_name
from src.helpers.environment_helper import get_aws_region
from boto3.dynamodb.conditions import Key

log = logging.getLogger()
log.setLevel(logging.INFO)
dynamo_client = None


def dynamo_lookup_item(keyword):
    log.info(f'Looking up {keyword}, in {get_st_table_name()}')
    global dynamo_client
    if not dynamo_client:
        dynamo_client = boto3.resource('dynamodb', region_name=get_aws_region())

    st_table = dynamo_client.Table(get_st_table_name())
    found_item = st_table.query(
        KeyConditionExpression=Key('keyword').eq(keyword)
    )

    result = ""
    items = found_item['Items']
    if len(items) is not 0:
        result = items[0]
        log.info(f'Found item in dynamo: {result}')

    return result


def dynamo_save_item(item):
    __dynamo_save_item(item, get_st_table_name())


def __dynamo_save_item(item_to_save, table_name):
    log.info(f'Persisting {item_to_save} into Dynamo {table_name}')
    global dynamo_client
    if not dynamo_client:
        dynamo_client = boto3.resource('dynamodb', region_name=get_aws_region())
    table = dynamo_client.Table(table_name)

    table.put_item(Item=item_to_save)

