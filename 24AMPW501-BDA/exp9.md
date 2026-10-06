# Experiment 9
**Title:** Data Visualization Using Python

## Aim
To create Line, Bar, Pie, Scatter and Box plots using the Python libraries Pandas and Matplotlib.

## Algorithm
1. Install and import the Pandas and Matplotlib libraries.
2. Create a sample dataset with Month, Sales and Profit for five months.
3. Draw a line chart to show how sales change month by month.
4. Draw a bar chart to compare sales between months.
5. Draw a pie chart to show each month's share of the total sales.
6. Draw a scatter plot to show the relation between sales and profit.
7. Draw a box plot to show the spread of the sales values.
8. Display all the plots and study them.

## Program (visualization.py)
```bash
pip install pandas matplotlib
```
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "Month":  ["Jan", "Feb", "Mar", "Apr", "May"],
    "Sales":  [120, 150, 180, 160, 210],
    "Profit": [20, 30, 42, 35, 50],
})

fig, ax = plt.subplots(2, 3, figsize=(14, 8))

ax[0, 0].plot(df["Month"], df["Sales"], marker="o")
ax[0, 0].set(title="Monthly Sales", xlabel="Month", ylabel="Sales")

ax[0, 1].bar(df["Month"], df["Sales"])
ax[0, 1].set(title="Sales by Month", xlabel="Month", ylabel="Sales")

ax[0, 2].pie(df["Sales"], labels=df["Month"], autopct="%1.1f%%")
ax[0, 2].set_title("Sales Distribution")

ax[1, 0].scatter(df["Sales"], df["Profit"])
ax[1, 0].set(title="Sales vs Profit", xlabel="Sales", ylabel="Profit")

ax[1, 1].boxplot(df["Sales"])
ax[1, 1].set(title="Sales Box Plot", ylabel="Sales")

ax[1, 2].axis("off")                    # empty 6th slot

plt.tight_layout()
plt.savefig("plots.png")                # works even if plt.show() has no window (WSL2)
plt.show()
```

## Execution
```bash
python visualization.py
```

## Output
Five plots are displayed in one window (also saved as `plots.png`): Line Chart, Bar Chart, Pie Chart, Scatter Plot and Box Plot.

## Result
All five plots were created successfully using Python. The line and bar charts show that sales were highest in May (210) and lowest in January (120). The pie chart shows May has the largest share of total sales (25.6%). The scatter plot shows that profit increases as sales increase. The box plot shows the median sales value is 160.
