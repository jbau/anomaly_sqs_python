# -*- coding: utf-8 -*-
"""
This module is glue code to help report Wavefront anomalies, as defined by Anomalies.avdl,
to SQS.  There, it should be dequeued by ADS and reported into the Anomaly store.
"""

import avro.protocol as protocol

from StdoutBase64Transceiver import StdoutBase64Transceiver

PROTOCOL = protocol.Parse(open("../avro/anomalies.avpr").read())

requestor = StdoutBase64Transceiver(PROTOCOL)

anomaly = {
    "customer": "test",
    "startMs": 1000,
    "endMs": 1001,
    "queryHash": "qh",
    "paramHash": "ph",
    "chartHash": "ch",
    "dashboardId": "dbId",
    "section": 0,
    "row": 0,
    "col": 0,
    "model": "model123",
    "imageLink": "http://link/",
    "originalStripes": [],
    "queryParams": {"a": "b"},
    "updatedMs": 100012
}

requestor.Request("reportAnomaly", {"input": anomaly})
