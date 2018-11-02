# -*- coding: utf-8 -*-
"""
This module is glue code to help report Wavefront anomalies, as defined by Anomalies.avdl,
to SQS.  There, it should be dequeued by ADS and reported into the Anomaly store.
"""

import avro.ipc as ipc
import avro.protocol as protocol

PROTOCOL = protocol.parse(open("../avro/anomalies.avpr").read())

client = ipc.Tr