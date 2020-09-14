from avrodefs.Anomaly import Anomaly
from sqs_writer.SQSAnomalyReporter import SQSAnomalyReporter

queue_name = "anomaly-reporting-dev-local"
region_name = "us-west-2"
reporter = SQSAnomalyReporter(queue_name, region_name=region_name)
anomaly = Anomaly(customer="localdev", start_ms=1575094971, end_ms=1575302331, query_hash="['sum(rate(ts(agent-metrics.points.*.queued, source=\"clover\")), customer, agent)']", param_hash="ph",
                  chart_hash="ch_ch", dashboard_id="dbid", section=0, row=0, col=0, model="model235__test",
                  image_link="https://s3-us-west-2.amazonaws.com/wavefront-ml-prod/training/mon/collector/2020/09/09/192H/FDB-Upgrade-KPIs/T663957066_-1237837100_1598919932_1599611132.png", metrics_used=["m1", "m2"], hosts_used=["h1", "h2"])
reporter.reportAnomaly(anomaly)
