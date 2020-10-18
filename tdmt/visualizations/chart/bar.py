from tdmt.visualizations.chart.chart import Tooltip, ChartOptions, PlotOptions, Series, Axis, Chart, Legend


class ChartBar:
    def __init__(self, categories, stacked=None, caption=None, **kwargs):
        self.title = None
        self.caption = caption
        self.chart_options = ChartOptions(chart_type="bar")

        if stacked:
            self.plot_options = PlotOptions(series={"stacking": "normal"})
        else:
            self.plot_options = PlotOptions()

        self.tooltip = Tooltip(
            point_format="{series.name}, {point.name}:"
            "<br/>"
            "<b>{point.display_value:.2f}{point.display_suffix} {point.unit}</b>"
        )
        self.x_axis = Axis(type="category", categories=categories)
        y_axis_title = kwargs.get("axis_y", "")
        self.y_axis = Axis(
            title={"text": y_axis_title}, legend={"layout": "vertical", "align": "right", "verticalAlign": "middle"},
        )

        self.series = Series(data=None)
        self.legend = Legend(enabled=False)

    def add_series(self, data):

        try:
            first_point = data[0]["data"][0]
        except IndexError:
            first_point = {}
        if "percent_value" in first_point:
            point_format = f'<span style="color:{{point.color}}">{{point.category}}</span>:<br/><b>{{point.percent_value:,.1f}}</b>%<br/>'
        else:
            point_format = '<span style="color:{{point.color}}">{point.category}</span>:<br/><b>{point.display_value:,.1f}{point.display_suffix}{point.unit}</b><br/>'
        self.tooltip = Tooltip(point_format=point_format, value_suffix="",)
        if len(data) > 1:
            self.legend = Legend(enabled=True)

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
