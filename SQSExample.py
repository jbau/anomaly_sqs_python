from avrodefs.Anomaly import Anomaly
from sqs_writer.SQSAnomalyReporter import SQSAnomalyReporter

queue_name = "anomaly-reporting-dev"
reporter = SQSAnomalyReporter(queue_name)
anomaly = Anomaly(customer="mycustomer", start_ms=1000, end_ms=1001, query_hash="query_hash_my_test", param_hash="ph",
                  chart_hash="ch_ch", dashboard_id="dbid", section=0, row=0, col=0, model="model123",
                  image_link="http://link")
reporter.reportAnomaly(anomaly)
