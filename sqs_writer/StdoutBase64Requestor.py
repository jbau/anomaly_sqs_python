"""
A test transceiver
"""
import base64
import sys

from avro.ipc import BaseRequestor

from DummyTransceiver import DummyTransceiver
from sqs_writer.NoHandshakeRequestor import NoHandshakeRequestor


class StdoutBase64Requestor(NoHandshakeRequestor):
    def __init__(self, proto):
        BaseRequestor.__init__(self, proto, DummyTransceiver())

    def issue_request(self, call_request, message_name, request_datum):
        sys.stdout.write(base64.b64encode(call_request).decode("utf-8"))
