import plotly.graph_objects as go

# Data
x = [
    "22年度営業利益",
    "為替変動",
    "原価改善",
    "販売面の影響",
    "諸経費の増減",
    "その他",
    "23年度営業利益",
]
y = [23992, -2550, 1500, -2100, 700, 436, 21977]
measure = [
    "absolute",
    "relative",
    "relative",
    "relative",
    "relative",
    "relative",
    "total",
]

# Create waterfall chart
fig = go.Figure(
    go.Waterfall(
        x=x,
        y=y,
        measure=measure,  # Setting the type for each entry (absolute, relative, total)
        text=[f"{val:,}" for val in y],  # Format the text with commas for large numbers
        textposition="outside",
        decreasing={"marker": {"color": "red"}},
        increasing={"marker": {"color": "green"}},
        totals={"marker": {"color": "blue"}},
    )
)

# Customize layout
fig.update_layout(
    title="営業利益変化図",
    yaxis_title="営業利益 (in millions)",
    waterfallgap=0.3,  # Adjust the gap between bars
    font=dict(size=24),  # Set font size to double the default
    title_font=dict(size=28),  # Larger title font size
    yaxis=dict(titlefont=dict(size=24)),  # Y-axis label size
    xaxis=dict(tickfont=dict(size=24)),  # X-axis tick label size
)

# Show plot
fig.show()
