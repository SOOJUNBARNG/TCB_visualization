import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Example data setup
data = {
    "brands": ["BYD Auto", "Tesla", "Wuling", "Volkswagen", "GAC Motor", "Others"],
    "q2_2021": [20, 30, 25, 15, 10, 0],
    "q3_2021": [25, 35, 20, 10, 5, 5],
    "q4_2021": [30, 40, 15, 10, 5, 0],
    "q1_2022": [35, 45, 10, 5, 2, 3],
    "q2_2022": [40, 50, 5, 3, 1, 1],
    "q3_2022": [45, 55, 0, 1, 0, 0],
}
df = pd.DataFrame(data)

# Check DataFrame structure
print(df.head())
print(df.columns)

final = pd.DataFrame(df["brands"])

# Calculate upper and lower boundaries for each quarter
for i, col in enumerate(
    ["q2_2021", "q3_2021", "q4_2021", "q1_2022", "q2_2022", "q3_2022"]
):
    ch1 = df.loc[:, ["brands", col]]
    ch1.sort_values(col, inplace=True)
    ch1[f"y{i}_upper"] = ch1[col].cumsum()
    ch1[f"y{i}_lower"] = (
        ch1[f"y{i}_upper"].shift(1).fillna(0)
    )  # Ensure NaN is filled with 0
    ch1[f"y{i}"] = ch1.apply(
        lambda x: (x[f"y{i}_upper"] + x[f"y{i}_lower"]) / 2, axis=1
    )
    final = final.merge(
        ch1[["brands", f"y{i}_upper", f"y{i}_lower", f"y{i}"]], on="brands"
    )

print(final)


def getupperlower(brand):
    # Get the DataFrame row for the specified brand
    ch1 = final.query("brands == @brand")

    upper_col = [col for col in ch1.columns if "upper" in col]
    lower_col = [col for col in ch1.columns if "lower" in col]
    upper_data = ch1[upper_col].values.tolist()[0]
    lower_data = ch1[lower_col].values.tolist()[0]

    # Use the last value of upper data as a placeholder for annotations
    annotate_place = upper_data[-1]  # Use the last value of the upper data

    return upper_data, lower_data, annotate_place


# Define colors
colors = {
    "BYD Auto": "#72c6e8",
    "Tesla": "#E41A37",
    "Wuling": "#5c606d",
    "Volkswagen": "#12618F",
    "GAC Motor": "#d9871b",
    "Others": "rgba(0,0,0,0.1)",
}
colors2 = [colors[brand] for brand in df["brands"]]

# creating x axis value for the line chart
x = (np.arange(6) + 1).tolist()  ## [1,2,3,4,5,6]
x_rev = x[::-1]  ## [6,5,4,3,2,1]
annotations = []

fig = go.Figure()

for i, brand in enumerate(df["brands"]):
    upper_col, lower_col, annotate_place = getupperlower(brand)
    y_upper = upper_col
    y_lower = lower_col[::-1]  # Reverse lower to match the order

    fig.add_trace(
        go.Scatter(
            x=x + [x[-1] + 1, x[-1] + 1] + x_rev,
            y=y_upper + [y_upper[-1], y_lower[0]] + y_lower,
            fill="toself",
            fillcolor=colors2[i],
            opacity=0.5,
            line_color="rgba(0,0,0,0.2)",
            showlegend=False,
            name=brand,
            line_shape="spline",
            mode="lines",
            hovertemplate=" ",
        )
    )

    annotations.append(
        dict(
            xref="paper",
            yref="y",
            x=-0.005,
            y=annotate_place,
            text=brand,
            align="right",
            xanchor="right",
            font=dict(family="Arial", size=14, color=colors2[i]),
            showarrow=False,
        )
    )

fig.show()

# Bar chart
ch1 = df.set_index("brands")
for i, j in enumerate(
    ["q2_2021", "q3_2021", "q4_2021", "q1_2022", "q2_2022", "q3_2022"]
):
    ch2 = pd.DataFrame(ch1.T.iloc[i])
    ch2.columns = [i + 1]
    ch2.sort_values(i + 1, ascending=True, inplace=True)

    fig_px = px.bar(ch2.T, color_discrete_map=colors, opacity=0.7, text_auto=True)
    fig_px.update_traces(hovertemplate="<b>%{x}</b>, %{value}%")
    fig_px.update_traces(
        textfont=dict(size=10, color="black"),
        textposition="auto",
        cliponaxis=False,
        texttemplate="%{value}%",
    )

    for trace in fig_px["data"]:
        fig.add_trace(trace)

# Update layout
fig.update_layout(barmode="stack", bargap=0.7, showlegend=False)
fig.update_layout(
    plot_bgcolor="#f2f3f4", paper_bgcolor="#f2f3f4", margin=dict(l=100, b=10, r=100)
)
fig.update_xaxes(
    range=[0.85, 6.15],
    tickmode="array",
    showticklabels=True,
    ticktext=["q2_2021", "q3_2021", "q4_2021", "q1_2022", "q2_2022", "q3_2022"],
    tickvals=[1, 2, 3, 4, 5, 6],
    fixedrange=True,
    title_font=dict(size=24),
)
fig.update_yaxes(range=[0, 101], showticklabels=False, showgrid=False, fixedrange=True)
fig.update_layout(annotations=annotations)
fig.update_layout(
    title="Global Passenger Electric Vehicle Market Share, Q2 2021 - Q3 2022",
    title_font=dict(size=28),
)

# Show plot
fig.show()
