from sqs_writer.SQSAnomalyReporter import SQSAnomalyReporter
from avrodefs.Anomaly import Anomaly


queue_name = "anomaly-reporting-dev"
reporter = SQSAnomalyReporter(queue_name)
anomaly = Anomaly(customer="test", start_ms=1000, end_ms=1001, query_hash="qh", param_hash="ph", chart_hash="ch",
                 dashboard_id="dbid", section=0, row=0, col=0, model="model123", image_link="http://link")
reporter.reportAnomaly(anomaly)
