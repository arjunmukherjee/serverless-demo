import os


def get_sns_arn():
    return os.environ['ST_SNS_ARN']


def get_environment():
    return os.environ['ST_ENVIRONMENT_NAME']


def get_aws_region():
    return os.environ['ST_AWS_REGION']


def get_slack_webhook():
    return os.environ['SLACK_WEBHOOK']
