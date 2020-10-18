from tdmt.visualizations.chart import ChartOptions, PlotOptions, Tooltip, Axis, Series, Chart, Legend


class ChartPie:
    def __init__(self, caption=None, **kwargs):
        self.title = None
        self.chart_options = ChartOptions(chart_type="pie")

        self.plot_options = PlotOptions(
            pie={
                "allowPointSelect": True,
                "cursor": "pointer",
                "dataLabels": {"enabled": False,},
                "showInLegend": True,
            }
        )

        self.tooltip = Tooltip(
            point_format="{series.name}, {point.name}:"
            "<br/>"
            "<b>{point.display_value:.2f}{point.display_suffix} {point.unit}</b>"
        )
        self.x_axis = Axis()
        self.y_axis = Axis()

        self.caption = caption

        self.series = Series(data=None)
        self.legend = Legend(enabled=True, maxHeight=120)

    def add_series(self, data):
        self.series = Series(data=data)

    def export_json(self):
        if self.series.data is None:
            raise NotImplementedError
        chart = Chart(
            tooltip=self.tooltip,
            chart_options=self.chart_options,
            plot_options=self.plot_options,
            series=self.series,
            x_axis=self.x_axis,
            y_axis=self.y_axis,
            title=self.title,
            legend=self.legend,
            caption=self.caption,
        )
        return chart()
