## EXP 2: Agile Runtime Model Drift Monitoring Dashboard

### AIM
To develop an Agile Runtime Monitoring Dashboard that continuously tracks AI model performance, detects runtime model drift, monitors automated system performance metrics such as CPU usage, memory usage, latency, and throughput, and visualizes these metrics using an interactive Plotly dashboard. ALGORITHM: 1. Import the required libraries such as Pandas, NumPy, and Plotly. 2. Create or load the runtime monitoring dataset. 3. Store the runtime metrics in a Pandas DataFrame. 4. Calculate the model drift score using the reference accuracy value. 5. Create an interactive dashboard using Plotly subplots. 6. Display the model accuracy trend. 7. Display the CPU and memory usage charts. 8. Display the prediction latency chart. 9. Display the model drift chart. 10. Display the latest runtime performance metrics. 11. Display the complete runtime metrics table. 12. Analyze the dashboard to monitor model drift and evaluate system performance.

### ALGORITHM


### PROGRAM
```python
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Runtime dataset
np.random.seed(42)
runtime = pd.DataFrame({
    "Time":       pd.date_range("2026-01-01", periods=30, freq="min"),
    "Accuracy":   np.random.uniform(92, 99, 30),
    "CPU":        np.random.uniform(20, 80, 30),
    "Memory":     np.random.uniform(30, 90, 30),
    "Latency":    np.random.uniform(40, 120, 30),
    "Throughput": np.random.uniform(100, 200, 30),
})
runtime["Drift"] = abs(runtime["Accuracy"] - 95)

# KPI summary
latest = runtime.iloc[-1]
print("------ Agile Runtime Dashboard ------")
print(f"Accuracy    : {latest.Accuracy:.2f}%")
print(f"CPU Usage   : {latest.CPU:.2f}%")
print(f"Memory      : {latest.Memory:.2f}%")
print(f"Latency     : {latest.Latency:.2f} ms")
print(f"Throughput  : {latest.Throughput:.2f} req/sec")
print(f"Drift Score : {latest.Drift:.2f}")
print("Status      :", "Drift Detected" if latest.Drift > 2 else "Normal")

# Dashboard
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Accuracy Trend", "CPU & Memory", "Latency", "Model Drift"),
)
t = runtime["Time"]

fig.add_trace(go.Scatter(x=t, y=runtime["Accuracy"], mode="lines+markers", name="Accuracy"), row=1, col=1)
fig.add_trace(go.Scatter(x=t, y=runtime["CPU"], name="CPU"), row=1, col=2)
fig.add_trace(go.Scatter(x=t, y=runtime["Memory"], name="Memory"), row=1, col=2)
fig.add_trace(go.Bar(x=t, y=runtime["Latency"], name="Latency"), row=2, col=1)
fig.add_trace(go.Scatter(x=t, y=runtime["Drift"], fill="tozeroy", name="Drift"), row=2, col=2)

fig.update_layout(height=800, title="Agile Runtime Monitoring Dashboard", template="plotly_dark")
fig.show()

# Metrics table
print("\nRuntime Metrics Table (last 5 rows)")
print(runtime.tail().to_string(index=False, float_format="%.2f"))
```

### OUTPUT
```text
------ Agile Runtime Dashboard ------
Accuracy    : 92.33%
CPU Usage   : 39.52%
Memory      : 58.33%
Latency     : 83.15 ms
Throughput  : 127.86 req/sec
Drift Score : 2.67
Status      : Drift Detected

Runtime Metrics Table (last 5 rows)
               Time  Accuracy   CPU  Memory  Latency  Throughput  Drift
2026-01-01 00:25:00     97.50 75.31   49.51   109.72      103.69   2.50
2026-01-01 00:26:00     93.40 25.31   73.78   104.29      160.96   1.60
2026-01-01 00:27:00     95.60 31.76   68.25    54.93      150.27   0.60
2026-01-01 00:28:00     96.15 22.71   83.23   111.40      105.15   1.15
2026-01-01 00:29:00     92.33 39.52   58.33    83.15      127.86   2.67
```

*The interactive 4-panel Plotly dashboard (accuracy trend, CPU and memory lines, latency bars, drift area chart) opens through `fig.show()`.*

### RESULT
The Agile Runtime Monitoring Dashboard was successfully developed. It displays model accuracy, CPU usage, memory usage, latency, throughput, and model drift using interactive charts and a data table.
