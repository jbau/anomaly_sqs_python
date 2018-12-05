# -*- coding: utf-8 -*-
"""
A Requestor for working with avro.ipc.request that sends to SQS
"""

import base64

import boto3
from avro.ipc import BaseRequestor

from DummyTransceiver import DummyTransceiver
from sqs_writer.NoHandshakeRequestor import NoHandshakeRequestor


class SQSRequestor(NoHandshakeRequestor):
    def __init__(self, proto, queue_name, aws_access_key_id=None, aws_secret_access_key=None):
        BaseRequestor.__init__(self, proto, DummyTransceiver())
        if aws_access_key_id is None or aws_secret_access_key is None:
            self.resource = boto3.resource('sqs')
        else:
            self.resource = boto3.resource('sqs',
                                           aws_access_key_id=aws_access_key_id,
                                           aws_secret_access_key=aws_secret_access_key)
        self.queue = self.resource.get_queue_by_name(QueueName=queue_name)

    def issue_request(self, call_request, message_name, request_datum):
        self.queue.send_message(MessageBody=base64.b64encode(call_request).decode("utf-8"))
