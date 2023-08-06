import importlib
from assertpy import assert_that

from deepdriver.sdk.chart.chart import Chart

def visualize(chart: Chart) -> None:
    assert_that(chart).is_not_none()

    plotly_path = "plotly.express"
    plotly_module = importlib.import_module(plotly_path)
    plotly_chart_func = getattr(plotly_module, chart.chart_type)

    fig = plotly_chart_func(
        x=chart.data.dataframe[chart.data_fields["x"]],
        y=chart.data.dataframe[chart.data_fields["y"]],
        labels=chart.data_fields,
        title=chart.label_fields["title"],
    )
    fig.show()
