# -*- coding: utf-8 -*-
"""
A Transceiver that for working with avro.ipc.request that sends to SQS
"""

import boto3

class SQSTransceiver():
    client = boto3.client('sqs')
