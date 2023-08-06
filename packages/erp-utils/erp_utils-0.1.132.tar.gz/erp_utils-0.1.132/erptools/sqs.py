import itertools
import logging
import os
from typing import Optional, List

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()


def get_sqs():
    """
    Return SQS resource, this is for not execute boto3 when run the tests
    :return: Resource SQS
    """
    endpoint_url = os.getenv('AWS_SQS_ENDPOINT_URL', None)
    use_ssl = os.getenv('AWS_SQS_USE_SSL', True)

    return boto3.resource(service_name='sqs', endpoint_url=endpoint_url, use_ssl=use_ssl, region_name="ca-central-1")


def create_queue(name, attributes=None):
    """
    Creates an Amazon SQS queue.

    :param name: The name of the queue. This is part of the URL assigned to the queue.
    :param attributes: The attributes of the queue, such as maximum message size or
                       whether it's a FIFO queue.
    :return: A Queue object that contains metadata about the queue and that can be used
             to perform queue operations like sending and receiving messages.
    """
    if not attributes:
        attributes = {}
    try:
        sqs = get_sqs()
        queue = sqs.create_queue(
            QueueName=name,
            Attributes=attributes
        )
        logger.info("Created queue '%s' with URL=%s", name, queue.url)
    except ClientError as error:
        logger.exception("Couldn't create queue named '%s'. %s", name, error)
        raise error
    else:
        return queue


def get_queue(name):
    """
    Gets an SQS queue by name.

    :param name: The name that was used to create the queue.
    :return: A Queue object.
    """
    try:
        sqs = get_sqs()
        queue = sqs.get_queue_by_name(QueueName=name)
        logger.info("Got queue '%s' with URL=%s", name, queue.url)
    except ClientError as error:
        if error.response["Error"]["Code"] == "AWS.SimpleQueueService.NonExistentQueue":
            attributes = {
                'MaximumMessageSize': str(4096),
                'ReceiveMessageWaitTimeSeconds': str(10),
                'VisibilityTimeout': str(300),
                'FifoQueue': str(True),
                'ContentBasedDeduplication': str(True)
            }
            return create_queue(name, attributes)
        else:
            logger.exception("Couldn't get queue named %s. %s", name, error)
            raise error
    else:
        return queue


def send_message(message_body, message_deduplication_id, queue_name, message_group_id='quickbook',
                 message_attributes=None):
    """
    Send a message to an Amazon SQS queue.

    :param message_group_id: String, The tag that specifies that a message belongs to a specific message group. Messages that belong to the same message group are processed in a FIFO manner (however, messages in different message groups might be processed out of order). To interleave multiple ordered streams within a single queue, use MessageGroupId values (for example, session data for multiple users). In this scenario, multiple consumers can process the queue, but the session data of each user is processed in a FIFO fashion.
    :param message_deduplication_id:  String, The token used for deduplication of sent messages. If a message with a particular MessageDeduplicationId is sent successfully, any messages sent with the same MessageDeduplicationId are accepted successfully but aren't delivered during the 5-minute deduplication interval. For more information, see Exactly-Once Processing in the Amazon Simple Queue Service Developer Guide .
    :param message_body: The body text of the message.
    :param message_attributes: Custom attributes of the message. These are key-value
                               pairs that can be whatever you want.
    :param queue_name: Name of SQS Queque
    :return: The response from SQS that contains the assigned message ID.
    """

    if not message_attributes:
        message_attributes = {}
    try:
        queue = get_queue(queue_name)

        if queue_name.lower().endswith(".fifo"):
            response = queue.send_message(
                MessageBody=message_body,
                MessageAttributes=message_attributes,
                MessageGroupId=message_group_id,
                MessageDeduplicationId=message_deduplication_id
            )
        else:
            response = queue.send_message(
                MessageBody=message_body,
                MessageAttributes=message_attributes,
            )
        logger.info("Send message sqs: queue_name:{}".format(queue_name))
    except ClientError as error:
        logger.exception("Send message failed: %s", error)
        raise error
    else:
        return response

def send_messages(entries: List[dict], queue_name: str):
    try:
        queue = get_queue(queue_name)
        for e in split_entries(entries):
            response = queue.send_messages(
                Entries=e
            )
            logger.info(f"Sending Batch messages sqs: queue_name:{queue_name}, entries_sent: {len(e)} ")
    except ClientError as error:
        logger.exception("Send messages failed: %s", error)
        raise error
    else:
        return response


def compile_message(message_id: str,
                    message_body: str,
                    delay_seconds: Optional[int] = None,
                    MessageAttributes=None,
                    message_system_attributes: Optional[dict] = None,
                    message_deduplication_id: Optional[str] = None,
                    message_group_id: Optional[str] = None,
                    ) -> dict:
    """

    :param message_id:
    :param message_body:
    :param delay_seconds:
    :param MessageAttributes:
    :param message_system_attributes:
    :param message_deduplication_id:
    :param message_group_id:
    :return:
    """
    if MessageAttributes is None:
        MessageAttributes = {}
    params = (
        ("Id", message_id),
        ("MessageBody", message_body),
        ("DelaySeconds", delay_seconds),
        ("MessageAttributes", MessageAttributes),
        ("MessageSystemAttributes", message_system_attributes),
        ("MessageDeduplicationId", message_deduplication_id),
        ("MessageGroupId", message_group_id),
    )
    return {key: value for key, value in filter(lambda pair: pair[1] is not None, params)}


def split_entries(iterable):
    """Maximum size of entries to a message queue is 10"""
    size = 10
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))
