POINT_FORMAT_DEFAULT = "{series.name}, {point.category}:<br/><b>{point.y}</b><br/>"


class Tooltip:
    def __init__(
        self, point_format: str, header_format: str = "", value_suffix: str = "", value_decimals: int = 2, **kwargs
    ) -> None:
        if point_format == "default":

            self.pointFormat = POINT_FORMAT_DEFAULT
        else:
            self.pointFormat = point_format
        self.headerFormat = header_format

        if value_suffix not in ["", "%"]:
            self.valueSuffix = " " + value_suffix
        else:
            self.valueSuffix = value_suffix
        self.valueDecimals = value_decimals
        self.__dict__.update(**kwargs)

    def __call__(self) -> dict:
        return self.__dict__


class Legend:
    def __init__(self, enabled: bool = True, **kwargs):
        self.enabled = enabled
        self.__dict__.update(**kwargs)

    def __call__(self) -> dict:
        return self.__dict__


class Axis:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def __call__(self) -> dict:
        return self.__dict__


class Series:
    def __init__(self, data):
        self.data = data

    def __call__(self) -> dict:
        return self.data


class PlotOptions:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def __call__(self) -> dict:
        return self.__dict__


class ChartOptions:
    def __init__(self, chart_type: str, inverted: bool = False, polar: bool = False, **kwargs):
        self.type = chart_type
        self.inverted = inverted
        self.polar = polar
        self.__dict__.update(**kwargs)

    def __call__(self):
        return self.__dict__


class Caption:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def __call__(self) -> dict:
        return self.__dict__


class Chart:
    def __init__(
        self,
        chart_options: ChartOptions,
        tooltip: Tooltip,
        plot_options: PlotOptions,
        series: Series,
        x_axis: Axis,
        y_axis: Axis,
        legend: Legend,
        title: str = None,
        caption: str = None,
        **kwargs
    ) -> None:

        self.chart_options = chart_options
        self.credits = {"enabled": False}
        self.exporting = {
            "chartOptions": {"plotOptions": {"series": {"dataLabels": {"enabled": False}}}},
            "fallbackToExportServer": False,
            "buttons": {"contextButton": {"menuItems": ["downloadPNG", "downloadSVG",]}},
        }
        self.tooltip = tooltip
        self.plot_options = plot_options
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.series = series
        self.legend = legend
        self.title = {"text": title}
        self.caption = {"text": caption}
        self.__dict__.update(**kwargs)

    def __call__(self, **kwargs) -> dict:
        chart = {
            "chart": self.chart_options(),
            "credits": self.credits,
            "exporting": self.exporting,
            "series": self.series(),
            "caption": self.caption,
            "title": self.title,
        }

        if self.tooltip is not None:
            chart["tooltip"] = self.tooltip()

        if self.plot_options is not None:
            chart["plotOptions"] = self.plot_options()

        if self.x_axis is not None:
            chart["xAxis"] = self.x_axis()

        if self.y_axis is not None:
            chart["yAxis"] = self.y_axis()

        if self.legend is not None:
            chart["legend"] = self.legend()

        return {**chart, **kwargs}
