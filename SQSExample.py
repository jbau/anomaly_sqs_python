from avrodefs.Anomaly import Anomaly
from sqs_writer.SQSAnomalyReporter import SQSAnomalyReporter

queue_name = "anomaly-reporting-dev-local"
region_name = "us-west-2"
reporter = SQSAnomalyReporter(queue_name, region_name=region_name)
anomaly = Anomaly(customer="xtong_test", start_ms=5000, end_ms=5001, query_hash="query_hash_xtong_test", param_hash="ph",
                  chart_hash="ch_ch", dashboard_id="dbid", section=0, row=0, col=0, model="model235",
                  image_link="https://wavefront-ml-dev.s3-us-west-2.amazonaws.com/training/local/collector/2019/02/03/24H/RepeatCycle/T0127Z_training_section_0_row_0_chart_0_1549067232_1549153632_params_0-scaled.png", metrics_used=["m1", "m2"], hosts_used=["h1", "h2"])
reporter.reportAnomaly(anomaly)
