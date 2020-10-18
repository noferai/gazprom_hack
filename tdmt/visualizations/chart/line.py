from tdmt.visualizations.chart.chart import Tooltip, ChartOptions, PlotOptions, Series, Axis, Chart, Legend


class LineChart:
    def __init__(self, chart_type=None, stacking=None, tooltip_format=None, caption=None, **kwargs):
        self.title = None
        if chart_type:
            self.chart_options = ChartOptions(chart_type=chart_type)
        else:
            self.chart_options = ChartOptions(chart_type="spline")
        if stacking:
            self.plot_options = PlotOptions(series={"stacking": stacking})
        else:
            self.plot_options = PlotOptions()
        if tooltip_format:
            self.tooltip = Tooltip(point_format=tooltip_format, value_suffix="")
        else:
            self.tooltip = Tooltip(
                point_format="{point.date_formatted}<br/> <b>{point.y:.2f} {point.unit}</b><br/>", value_suffix="",
            )

        self.caption = caption

        x_axis_type = kwargs.get("x_axis_type", None)

        if x_axis_type:
            self.x_axis = Axis(allowDecimals=False, type=x_axis_type)
        else:
            self.x_axis = Axis(allowDecimals=False)
        y_axis_title = kwargs.get("axis_y", None)
        if y_axis_title:
            self.y_axis = Axis(
                title={"text": y_axis_title},
                legend={"layout": "vertical", "align": "right", "verticalAlign": "middle"},
            )
        else:
            self.y_axis = Axis()
        x_axis_title = kwargs.get("axis_x", None)
        if x_axis_title:
            self.x_axis = Axis(
                title={"text": x_axis_title},
                legend={"layout": "vertical", "align": "right", "verticalAlign": "middle"},
            )
        self.series = Series(data=None)
        self.legend = Legend()

    def add_series(self, data):
        self.series = Series(data=data)
        if len(data) == 1:
            self.legend = Legend(enabled=False)

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
