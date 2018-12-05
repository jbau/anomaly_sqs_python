"""
Plain python class representing an anomaly object
"""
import copy


class Anomaly(object):
    def __init__(self, customer, start_ms, end_ms, query_hash, param_hash, chart_hash,
                 dashboard_id, section, row, col, model="N/A", image_link="N/A",
                 query_params={}):
        self.customer = customer
        self.startMs = start_ms
        self.endMs = end_ms
        self.queryHash = query_hash
        self.paramHash = param_hash
        self.chartHash = chart_hash
        self.dashboardId = dashboard_id
        self.section = section
        self.row = row
        self.col = col
        self.model = model
        self.imageLink = image_link
        self.queryParams = copy.copy(query_params)
        self.updatedMs = 0  # placeholder values that can't be set
        self.originalStripes = []  # placeholder values that can't be set
