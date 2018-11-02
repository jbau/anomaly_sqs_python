# -*- coding: utf-8 -*-
"""
This module is glue code to help report Wavefront anomalies, as defined by Anomalies.avdl,
to SQS.  There, it should be dequeued by ADS and reported into the Anomaly store.
"""

import avro.protocol as protocol

from avrodefs.Anomaly import Anomaly
from sqs_writer.StdoutBase64Requestor import StdoutBase64Requestor

PROTOCOL = protocol.Parse(open("avrodefs/anomalies.avpr").read())
anomaly = Anomaly(customer="test", start_ms=1000, end_ms=1001, query_hash="qh", param_hash="ph", chart_hash="ch",
                  dashboard_id="dbid", section=0, row=0, col=0, model="model123", image_link="http://link")

if __name__ == "__main__":
    requestor = StdoutBase64Requestor(PROTOCOL)
    requestor.Request("reportAnomaly", {"input": vars(anomaly)})
