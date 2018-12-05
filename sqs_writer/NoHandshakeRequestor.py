# -*- coding: utf-8 -*-
"""
A Requestor that omits the Avro Handshake, which is apparently what Wavefront avro SQS does
"""
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from avro import io
from avro.ipc import BaseRequestor


class NoHandshakeRequestor(BaseRequestor):
    def request(self, message_name, request_datum):
        """
        Writes a request message and reads a response or error message.  Skips the handshake
        """
        # build call request
        buffer_writer = StringIO()
        buffer_encoder = io.BinaryEncoder(buffer_writer)
        self.write_call_request(message_name, request_datum, buffer_encoder)

        # send the call request; block until call response
        call_request = buffer_writer.getvalue()
        return self.issue_request(call_request, message_name, request_datum)
