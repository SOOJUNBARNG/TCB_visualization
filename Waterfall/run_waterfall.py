import matplotlib.pyplot as plt
import numpy as np

# Data
x = [
    "19年度営業利益",
    "為替変動",
    "原価改善",
    "販売面の影響",
    "諸経費の増減",
    "その他",
    "20年度営業利益",
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

# Calculating cumulative sum for waterfall effect
y_cumsum = np.zeros(len(y))
y_cumsum[0] = y[0]  # starting with absolute profit for 19年度営業利益
for i in range(1, len(y)):
    if measure[i] == "total":
        y_cumsum[i] = y[i]  # total for 20年度営業利益
    else:
        y_cumsum[i] = y_cumsum[i - 1] + y[i]  # cumulative for relative measures

# Create the waterfall chart
fig, ax = plt.subplots()

# Bars for relative values
for i in range(1, len(y) - 1):
    color = "green" if y[i] >= 0 else "red"
    ax.bar(x[i], y[i], bottom=y_cumsum[i - 1], color=color)

# Bars for absolute and total
ax.bar(x[0], y[0], color="blue")  # absolute start
ax.bar(x[-1], y[-1], color="blue")  # total end

# Connecting lines
for i in range(1, len(y)):
    ax.plot(
        [x[i - 1], x[i]],
        [y_cumsum[i - 1], y_cumsum[i - 1]],
        color="black",
        linestyle="--",
    )

# Formatting
plt.xticks(rotation=45, ha="right")
plt.ylabel("営業利益")
plt.title("Waterfall Chart of 営業利益 Changes")
plt.show()
