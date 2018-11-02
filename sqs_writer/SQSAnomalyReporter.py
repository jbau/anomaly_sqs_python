# -*- coding: utf-8 -*-
"""
A library that reports anomalies to sqs
"""
import os
from avro import protocol

from avrodefs.Anomaly import Anomaly
from sqs_writer.SQSRequestor import SQSRequestor

PROTOCOL_PATH = os.path.join(os.path.dirname(__file__), "../avrodefs/anomalies.avpr")
PROTOCOL = protocol.Parse(open(PROTOCOL_PATH).read())


class SQSAnomalyReporter(object):
    def __init__(self, queue_name, aws_access_key_id=None, aws_secret_access_key=None):
        self.requestor = SQSRequestor(PROTOCOL, queue_name, aws_access_key_id, aws_secret_access_key)

    def reportAnomaly(self, anomaly: Anomaly):
        self.requestor.Request("reportAnomaly", {"input": vars(anomaly)})
