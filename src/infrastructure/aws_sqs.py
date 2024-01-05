import json
import logging
import boto3

END_POINT_URL = "http://localhost:4566"
SQS_QUEUE_URL = "http://localhost:4566/000000000000/process"


def send_sqs_message(message):
    sqs_client = boto3.client("sqs", endpoint_url=END_POINT_URL)

    response = sqs_client.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(message)
    )
    logging.info(response)


def create_sqs_queue(name):
    sqs_client = boto3.client("sqs", endpoint_url=END_POINT_URL)

    response = sqs_client.create_queue(
        QueueName=name,
        Attributes={'string': 'string'},
        tags={'string': 'string'}
    )
    logging.info(response)
