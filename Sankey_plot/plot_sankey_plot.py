from bokeh.models import HoverTool
import holoviews as hv
from holoviews import opts, dim
import pandas as pd

hv.extension("bokeh")

# 上位30ペアのみ（単位：キロトン）
sparklingwine = [
    ["Europe", "France", "North America", "USA", 736],
    ["Europe", "France", "Europe", "UK", 520],
    ["Europe", "Italy", "Europe", "UK", 513],
    ["Europe", "Italy", "North America", "USA", 394],
    ["Europe", "France", "Asia", "Singapore", 337],
    ["Europe", "France", "Europe", "Germany", 317],
    ["Asia", "Singapore", "Asia", "Japan", 225],
    ["Europe", "France", "Asia", "Japan", 207],
    ["Europe", "France", "Europe", "Belgium", 193],
    ["Europe", "France", "Europe", "Italy", 190],
    ["Europe", "France", "Europe", "Switzerland", 132],
    ["Europe", "Italy", "Europe", "Germany", 121],
    ["Europe", "France", "Europe", "Spain", 103],
    ["Europe", "France", "Oceania", "Australia", 103],
    ["Europe", "Spain", "North America", "USA", 90],
    ["Europe", "Spain", "Europe", "Germany", 85],
    ["Europe", "France", "Europe", "Sweden", 81],
    # ["Europe", "France", "North America", "Canada", 78],
    # ["Asia", "Singapore", "Oceania", "Australia", 72],
    # ["Europe", "France", "Europe", "Netherlands", 71],
    # ["Europe", "Italy", "Europe", "Switzerland", 71],
    # ["Europe", "Spain", "Europe", "Belgium", 70],
    # ["Europe", "Spain", "Europe", "UK", 65],
    # ["Europe", "Italy", "Europe", "France", 63],
    # ["Europe", "France", "Middle East", "UAE", 59],
    # ["Europe", "Italy", "Europe", "Russia", 56],
    # ["Europe", "Italy", "Europe", "Belgium", 54],
    # ["Europe", "Italy", "Europe", "Sweden", 50],
    # ["Europe", "Spain", "Europe", "France", 44],
    # ["Europe", "Italy", "North America", "Canada", 43],
    # ["Europe", "Italy", "Asia", "Japan", 40],
    # ["Europe", "Spain", "Asia", "Japan", 39],
    # ["Europe", "France", "Asia", "Hong Kong", 39],
    # ["Europe", "France", "Europe", "Denmark", 38],
    # ["Europe", "France", "Europe", "Austria", 37],
    # ["Europe", "Netherlands", "Asia", "Japan", 34],
]
sparklingwine_df = pd.DataFrame(sparklingwine).rename(
    {0: "region_exp", 1: "country_exp", 2: "region_imp", 3: "country_imp", 4: "value"},
    axis="columns",
)


def set_exp(df):
    if df.country_exp in ["Singapore", "Netherlands"]:
        return df.country_exp
    else:
        return df.country_exp + " Exp"


sparklingwine_df = sparklingwine_df.assign(
    country_exp=lambda x: x.apply(set_exp, axis=1)
)

hover = HoverTool(
    tooltips=[
        ("From", "@country_exp"),
        ("To", "@country_imp"),
        ("Value [kt]", "@value"),
    ]
)

sparklingwine_sankey = hv.Sankey(
    sparklingwine_df,
    kdims=["country_exp", "country_imp"],
    vdims=["value"],
    label="World's Top Sparkling Wine Trade Routes in 2018 (Value in million USD)",
).opts(
    width=900,
    height=800,
    cmap="glasbey_hv",
    edge_line_alpha=0,
    edge_color=dim("country_exp").str(),
    tools=[hover],
    node_sort=True,
) * hv.Text(
    500,
    -15,
    "Based on AAWE's post on Facebook https://www.facebook.com/wineecon/posts/3557583497601764/",
    fontsize=10,
)

hv.save(sparklingwine_sankey, "sparklingwine_sankey.html")
