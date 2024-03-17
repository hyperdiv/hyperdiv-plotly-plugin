import os
import json
import plotly
import plotly.graph_objects as go
import hyperdiv as hd


class PlotlyFigDef(hd.HyperdivType):
    def parse(self, value):
        if not isinstance(value, go.Figure):
            raise ValueError(
                f"Expected a `plotly.graph_objects.Figure` but got {type(value)}"
            )
        return value

    def render(self, value):
        return json.loads(plotly.io.to_json(value))


class DictDef(hd.HyperdivType):
    def parse(self, value):
        if not isinstance(value, dict):
            raise ValueError(f"Expected a `dict` but got {type(value)}")
        return value


PlotlyFig = PlotlyFigDef()
Dict = DictDef()


class plotly_chart(hd.Plugin):
    _assets_root = os.path.join(os.path.dirname(__file__), "assets")

    _assets = [
        "plotly.css",
        "plotly-2.29.1.min.js",
        "hyperdiv-plotly-plugin.js",
    ]

    fig = hd.Prop(PlotlyFig)
    browser_config = hd.Prop(Dict)

    def __init__(self, fig, browser_config=None, **kwargs):
        super().__init__(
            fig=fig,
            browser_config=(browser_config or self.get_default_browser_config()),
            **kwargs,
        )

    @staticmethod
    def get_default_browser_config():
        return dict(
            responsive=True,
            displayModeBar=False,
            modeBarButtonsToRemove=["lasso2d", "select2d"],
        )

    @staticmethod
    def get_default_layout(margin=dict(l=0, r=0, t=0, b=0)):
        theme = hd.theme()

        if theme.is_dark:
            label_color = "rgba(255, 255, 255, 0.5)"
            color = "rgba(255, 255, 255, 0.1)"
        else:
            label_color = "rgba(0, 0, 0, 0.5)"
            color = "rgba(0, 0, 0, 0.1)"

        return {
            "autosize": True,
            "margin": margin,
            "plot_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent background
            "paper_bgcolor": "rgba(0, 0, 0, 0)",  # Transparent paper
            "font_color": label_color,  # Text color
            "xaxis": {
                "color": label_color,
                "gridcolor": color,  # Gridline color
                "linecolor": color,
            },
            "yaxis": {
                "color": label_color,
                "gridcolor": color,
                "linecolor": color,
                "zeroline": False,
            },
        }
