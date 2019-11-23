import boto3
import logging
import json
import uuid

from datetime import datetime
from src.helpers.environment_helper import get_aws_region
from src.kinesis.kinesis_helper import get_st_stream_name

log = logging.getLogger()
log.setLevel(logging.INFO)
kinesis_client = None


def kinesis_put_item(item):
    item_id = str(uuid.uuid4())
    log.info(f'Persisting {item} into Kinesis with id {item_id}')
    global kinesis_client
    if not kinesis_client:
        kinesis_client = boto3.client('kinesis', region_name=get_aws_region())

    payload = {
        'item': item,
        'timestamp': str(datetime.now()),
        'item_id': item_id
    }

    log.info(payload)

    kinesis_client.put_record(
        StreamName=get_st_stream_name(),
        Data=json.dumps(payload),
        PartitionKey=item_id)
