from tdmt.visualizations.chart import ChartPie, LineChart


def prepare_visualisation(chart_type, **kwargs):
    visualization = viz_json = None

    if chart_type == "chart_line":
        visualization = LineChart()
    elif chart_type == "chart_pie":
        visualization = ChartPie()

    if visualization:
        visualization.add_series(data=series)
        viz_json = visualization.export_json()

    if viz_json is not None:
        result = {"data": {"type": chart_type, "attributes": viz_json}}
        return result
