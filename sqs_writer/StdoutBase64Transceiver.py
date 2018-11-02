"""
A test transceiver
"""
import base64
import io
import sys

from avro import io as avro_io
from avro.ipc import Transceiver, META_WRITER, BaseRequestor


class StdoutBase64Transceiver(BaseRequestor):
    def __init__(self, proto):
        BaseRequestor.__init__(self, proto, None)
        self.proto = proto

    def _IssueRequest(self, call_request, message_name, request_datum):
        sys.stdout.write(base64.b64encode(call_request).decode("utf-8"))
