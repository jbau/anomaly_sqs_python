"""
A test transceiver
"""
import base64
import sys

from avro.ipc import BaseRequestor


class StdoutBase64Requestor(BaseRequestor):
    def __init__(self, proto):
        BaseRequestor.__init__(self, proto, None)

    def _IssueRequest(self, call_request, message_name, request_datum):
        sys.stdout.write(base64.b64encode(call_request).decode("utf-8"))
