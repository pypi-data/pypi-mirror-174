import json
from assertpy import assert_that
from typing import Dict

from deepdriver.sdk.data_types.dataFrame import DataFrame

TYPE_HISTOGRAM = "histogram"
TYPE_LINE = "line"
TYPE_SCATTER = "scatter"

class Chart:

    def __init__(self, data: DataFrame, chart_type: str, data_fields: Dict, label_fields: Dict=None) -> None:
        assert_that(data).is_not_none()
        assert_that(chart_type).is_not_none()
        assert_that(data_fields).is_not_none()

        self.data = data
        self.log_type = "chart"
        self.chart_type = chart_type
        self.data_fields = data_fields
        self.label_fields = label_fields if label_fields else {}

    def to_json(self, key_name: str) -> str:
        assert_that(key_name).is_not_none()

        value_type = __class__.__name__
        return json.dumps({
            "log_type" : self.log_type,
            "chart_type" : self.chart_type,
            "data_fields" : self.data_fields,
            "label_fields" : self.label_fields,
            "path" : self.get_path(key_name, value_type),
        })

    def upload(self) -> None:
        pass

    def upload_file(self) -> None:
        pass

    def get_path(self, key_name: str, value_type: str) -> str:
        return f"{key_name}.{value_type}.json"
