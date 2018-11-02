"""
Plain python class representing an anomaly object
"""
from typing import Dict


class Anomaly(object):
    def __init__(self, customer: str, start_ms: int, end_ms: int, query_hash: str, param_hash: str, chart_hash: str,
                 dashboard_id: str, section: int, row: int, col: int, model: str = "N/A", image_link: str = "N/A",
                 query_params: Dict[str, str] = {}):
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
        self.queryParams = query_params
        self.updatedMs = 0  # placeholder values that can't be set
        self.originalStripes = []  # placeholder values that can't be set
