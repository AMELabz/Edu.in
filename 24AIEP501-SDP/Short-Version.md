# SOFTWARE DESIGN PATTERN FOR INTELLIGENT AUTOMATION LABORATORY (24AIEP501)

## Shortened Programs — Experiments 1–12


---

## EXP 1: Automated DevOps Pipeline with Blue-Green Deployment

### AIM
To build a Blue-Green deployment pipeline for an IDP scoring model with traffic switching and rollback.

### ALGORITHM
1. Install the required Python libraries.
2. Create an IDP dataset with the following features:
   - Pages
   - Words
   - Images
   - Tables
   - Score
3. Train the Blue Model using the dataset.
4. Save the Blue model as model_blue.pkl.
5. Create a modified dataset and train the Green Model.
6. Save the Green model as model_green.pkl.
7. Load both models and set Blue as the active deployment.
8. Predict the document score using the active model.

### COMMAND/PROGRAM
Install: `python -m pip install numpy pandas scikit-learn joblib`  |  Run: `python exp1.py`

```python
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# ---------- Create IDP dataset ----------
np.random.seed(42)
FEATURES = ["Pages", "Words", "Images", "Tables"]

data = pd.DataFrame({
    "Pages":  np.random.randint(1, 50, 200),
    "Words":  np.random.randint(100, 5000, 200),
    "Images": np.random.randint(0, 20, 200),
    "Tables": np.random.randint(0, 10, 200),
})
data["Score"] = (
    data["Pages"] * 0.5
    + data["Words"] * 0.01
    + data["Images"] * 1.5
    + data["Tables"] * 2
)

# ---------- Train and save BLUE model ----------
blue = LinearRegression().fit(data[FEATURES], data["Score"])
joblib.dump(blue, "model_blue.pkl")

# ---------- Train and save GREEN model (modified data) ----------
data_green = data.copy()
data_green["Words"] *= 1.02
green = LinearRegression().fit(data_green[FEATURES], data_green["Score"])
joblib.dump(green, "model_green.pkl")

# ---------- Deploy ----------
models = {
    "BLUE": joblib.load("model_blue.pkl"),
    "GREEN": joblib.load("model_green.pkl"),
}
active = "BLUE"


def predict(*values):
    row = pd.DataFrame([values], columns=FEATURES)
    score = models[active].predict(row)[0]
    print(f"[{active}] Predicted Score: {score:.2f}")


document = (10, 1200, 3, 2)

print("Models trained and saved. Active:", active)
predict(*document)

active = "GREEN"
print("Traffic switched to", active)
predict(*document)

active = "BLUE"
print("Rollback to", active)
predict(*document)
```

### OUTPUT
```text
Models trained and saved. Active: BLUE
[BLUE] Predicted Score: 25.50
Traffic switched to GREEN
[GREEN] Predicted Score: 25.26
Rollback to BLUE
[BLUE] Predicted Score: 25.50
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 2: Agile Runtime Model Drift Monitoring Dashboard

### AIM
To monitor model accuracy, CPU, memory, latency, throughput and drift using an interactive Plotly dashboard.

### ALGORITHM


### COMMAND/PROGRAM
Install: `python -m pip install numpy pandas plotly`  |  Run: `python exp2.py`

```python
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------- Runtime dataset ----------
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

# ---------- KPI summary ----------
latest = runtime.iloc[-1]
print("------ Agile Runtime Dashboard ------")
print(f"Accuracy    : {latest.Accuracy:.2f}%")
print(f"CPU Usage   : {latest.CPU:.2f}%")
print(f"Memory      : {latest.Memory:.2f}%")
print(f"Latency     : {latest.Latency:.2f} ms")
print(f"Throughput  : {latest.Throughput:.2f} req/sec")
print(f"Drift Score : {latest.Drift:.2f}")
print("Status      :", "Drift Detected" if latest.Drift > 2 else "Normal")

# ---------- Dashboard ----------
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

fig.update_layout(
    height=800,
    title="Agile Runtime Monitoring Dashboard",
    template="plotly_dark",
)
fig.show()

# ---------- Metrics table ----------
print("\nRuntime Metrics Table (last 5 rows)")
print(runtime.tail().round(2).to_string(index=False))
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
/tmp/tmpy6fmhuwc/prog.py:54: UserWarning: obj.round has no effect with datetime, timedelta, or period dtypes. Use obj.dt.round(...) instead.
  print(runtime.tail().round(2).to_string(index=False))
(The 4-panel interactive Plotly dashboard opens via fig.show(): accuracy trend, CPU & memory lines, latency bars, drift area chart.)
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 3: SRS for Smart Warehouse Sorting Robot

### AIM
To draft an SRS for a warehouse sorting robot and map multi-threaded failure modes with mitigations.

### ALGORITHM
1. Identify the stakeholders of the warehouse sorting system.
2. Define the functional requirements of the robot.
3. Define non-functional requirements such as performance, reliability, safety and scalability.
4. Identify the different threads running simultaneously in the robot.
5. Analyze possible failure modes for each thread.
6. Document the mitigation strategy for every failure.
7. Prepare the Software Requirement Specification (SRS).
8. Verify the completeness of the SRS.

### COMMAND/PROGRAM
No external packages required. Run: `python exp3.py`

```python
functional = [
    "Scan incoming package",
    "Identify barcode/QR code",
    "Determine destination",
    "Sort package",
    "Update inventory database",
    "Generate delivery status",
]

non_functional = {
    "Performance":  "Sort 100 packages/minute",
    "Reliability":  "99.9% uptime",
    "Safety":       "Emergency stop support",
    "Scalability":  "Supports multiple robots",
    "Availability": "24x7 operation",
}

# thread -> (failure mode, mitigation)
failures = {
    "Sensor Thread":   ("Sensor Failure",            "Restart Sensor"),
    "Camera Thread":   ("Image Capture Failure",     "Capture Again"),
    "Barcode Thread":  ("Barcode Not Detected",      "Manual Verification"),
    "Sorting Thread":  ("Mechanical Jam",            "Stop Conveyor and Alert Operator"),
    "Database Thread": ("Database Connection Lost",  "Reconnect Database"),
    "Network Thread":  ("Communication Failure",     "Retry Network Connection"),
}

print("SYSTEM: Smart Warehouse Sorting Robot")

print("\nFunctional Requirements")
for item in functional:
    print("-", item)

print("\nNon-Functional Requirements")
for name, value in non_functional.items():
    print(f"{name} : {value}")

print("\nFailure Modes -> Mitigation")
for thread, (failure, fix) in failures.items():
    print(f"{thread} -> {failure} -> {fix}")
```

### OUTPUT
```text
SYSTEM: Smart Warehouse Sorting Robot

Functional Requirements
- Scan incoming package
- Identify barcode/QR code
- Determine destination
- Sort package
- Update inventory database
- Generate delivery status

Non-Functional Requirements
Performance : Sort 100 packages/minute
Reliability : 99.9% uptime
Safety : Emergency stop support
Scalability : Supports multiple robots
Availability : 24x7 operation

Failure Modes -> Mitigation
Sensor Thread -> Sensor Failure -> Restart Sensor
Camera Thread -> Image Capture Failure -> Capture Again
Barcode Thread -> Barcode Not Detected -> Manual Verification
Sorting Thread -> Mechanical Jam -> Stop Conveyor and Alert Operator
Database Thread -> Database Connection Lost -> Reconnect Database
Network Thread -> Communication Failure -> Retry Network Connection
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 4: Polymorphic Sensor Hardware Wrapper

### AIM
To build an abstract sensor wrapper using polymorphism to process different sensor types dynamically.

### ALGORITHM
1. Import the Abstract Base Class module.
2. Create an abstract class named Sensor.
3. Define an abstract method read_data().
4. Create subclasses for Temperature, Humidity and Motion sensors.
5. Override the read_data() method in each subclass.
6. Store all sensor objects in a list.
7. Access every sensor through the base class reference.
8. Display the sensor values using polymorphism.

### COMMAND/PROGRAM
No external packages required. Run: `python exp4.py`

```python
import random
from abc import ABC, abstractmethod


class Sensor(ABC):
    @abstractmethod
    def read_data(self):
        pass


class TemperatureSensor(Sensor):
    def read_data(self):
        return f"Temperature : {random.randint(25, 40)} C"


class HumiditySensor(Sensor):
    def read_data(self):
        return f"Humidity    : {random.randint(40, 80)} %"


class MotionSensor(Sensor):
    def read_data(self):
        state = random.choice(["Detected", "Not Detected"])
        return f"Motion      : {state}"


sensors = [TemperatureSensor(), HumiditySensor(), MotionSensor()]

print("====== Smart Warehouse Sensors ======")
for sensor in sensors:
    print(sensor.read_data())
```

### OUTPUT
```text
====== Smart Warehouse Sensors ======
Temperature : 36 C
Humidity    : 50 %
Motion      : Not Detected
(Values are random, so they change on every run.)
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 5: UML Sequence and Statechart for Drone Delivery

### AIM
To generate UML sequence and statechart diagrams for an autonomous drone delivery system.

### ALGORITHM
1. Import the required Python library.
2. Define the sequence diagram participants.
3. Generate the UML Sequence Diagram.
4. Define the states of the drone.
5. Generate the UML Statechart Diagram.
6. Display both diagrams.
7. End the process.

### COMMAND/PROGRAM
Install Python package: `pip install graphviz`; install the Graphviz system application and add `dot` to PATH. Run: `python exp5.py`

```python
from graphviz import Digraph

# ---------- Sequence diagram ----------
sequence = Digraph("SequenceDiagram", format="png")
sequence.attr(rankdir="LR")

for participant in ["Customer", "MobileApp", "Warehouse", "Drone"]:
    sequence.node(participant, shape="box")

messages = [
    ("Customer",  "MobileApp", "1. Place Order"),
    ("MobileApp", "Warehouse", "2. Send Order"),
    ("Warehouse", "Drone",     "3. Assign Delivery"),
    ("Drone",     "Customer",  "4. Deliver Package"),
    ("Customer",  "MobileApp", "5. Confirm Delivery"),
]
for sender, receiver, label in messages:
    sequence.edge(sender, receiver, label=label)

sequence.render("SequenceDiagram", view=False)

# ---------- Statechart diagram ----------
statechart = Digraph("StatechartDiagram", format="png")
statechart.attr(rankdir="LR")

states = ["Idle", "TakeOff", "Flying", "Delivering", "Returning", "Charging"]
for state in states:
    statechart.node(state, shape="circle")

for current, following in zip(states, states[1:] + states[:1]):
    statechart.edge(current, following)

statechart.render("StatechartDiagram", view=False)

print("UML DIAGRAMS GENERATED SUCCESSFULLY")
print("Files: SequenceDiagram.png, StatechartDiagram.png")
```

### OUTPUT
```text
UML DIAGRAMS GENERATED SUCCESSFULLY
Files: SequenceDiagram.png, StatechartDiagram.png
(Diagrams: Customer -> MobileApp -> Warehouse -> Drone -> Customer messages; states Idle -> TakeOff -> Flying -> Delivering -> Returning -> Charging -> Idle.)
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 6: Singleton Telemetry Manager and Abstract Factory

### AIM
To implement a thread-safe Singleton telemetry manager and a factory that creates Web, Desktop and Mobile drivers.

### ALGORITHM
1. Import the required library.
2. Create a Thread-safe Singleton Telemetry Manager.
3. Define Web, Desktop, and Mobile driver classes.
4. Create an Abstract Factory.
5. Instantiate different drivers using the factory.
6. Display the created drivers.
7. End the process.

### COMMAND/PROGRAM
No external packages required. Run: `python exp6.py`

```python
import threading


class TelemetryManager:
    """Thread-safe Singleton."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, message):
        print("Telemetry :", message)


class WebDriver:
    def start(self):
        print("Web Driver Started")


class DesktopDriver:
    def start(self):
        print("Desktop Driver Started")


class MobileDriver:
    def start(self):
        print("Mobile Driver Started")


class DriverFactory:
    drivers = {"Web": WebDriver, "Desktop": DesktopDriver, "Mobile": MobileDriver}

    @staticmethod
    def create_driver(kind):
        return DriverFactory.drivers[kind]()


telemetry = TelemetryManager()
telemetry.log("Application Started")
print("Same instance:", telemetry is TelemetryManager())

for kind in ["Web", "Desktop", "Mobile"]:
    DriverFactory.create_driver(kind).start()

telemetry.log("All Drivers Created Successfully")
```

### OUTPUT
```text
Telemetry : Application Started
Same instance: True
Web Driver Started
Desktop Driver Started
Mobile Driver Started
Telemetry : All Drivers Created Successfully
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 7: Adapter Design Pattern for JSON, XML and CSV Employee Data

### AIM
To read employee data from JSON, XML and CSV files through a common interface using the Adapter pattern.
(Note: the manual's title for Exp 7 repeats Exp 1; the content is the Adapter pattern.)

### ALGORITHM
1. Import the required Python libraries (json, csv, xml.etree.ElementTree, and abc).
2. Create an abstract class DataSource containing the abstract method get_data().
3. Create the JSONData class to read employee records from the emp.json file.
4. Create the XMLData class to read employee records from the emp.xml file.
5. Create the CSVData class to read employee records from the emp.csv file.
6. Implement JSONAdapter, XMLAdapter, and CSVAdapter classes that convert the different data sources into the common get_data() interface.
7. Create the AutomationPipeline class to process and display the records received through the adapters.
8. Instantiate the adapters for the JSON, XML, and CSV data sources.

### COMMAND/PROGRAM
No external packages required. The program creates `emp.json`, `emp.xml` and `emp.csv`. Run: `python exp7.py`

```python
import csv
import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

# ---------- Create sample files ----------
with open("emp.json", "w") as f:
    f.write('{"employees": [{"id": 101, "name": "Alice"}, {"id": 102, "name": "Bob"}]}')

with open("emp.xml", "w") as f:
    f.write(
        "<employees>"
        "<employee><id>201</id><name>Charlie</name></employee>"
        "<employee><id>202</id><name>David</name></employee>"
        "</employees>"
    )

with open("emp.csv", "w") as f:
    f.write("id,name\n301,Eve\n302,Frank\n")


# ---------- Target interface ----------
class DataSource(ABC):
    @abstractmethod
    def get_data(self):
        pass


# ---------- Adapters ----------
class JSONAdapter(DataSource):
    def get_data(self):
        with open("emp.json") as f:
            return json.load(f)["employees"]


class XMLAdapter(DataSource):
    def get_data(self):
        root = ET.parse("emp.xml").getroot()
        return [
            {"id": e.find("id").text, "name": e.find("name").text}
            for e in root.findall("employee")
        ]


class CSVAdapter(DataSource):
    def get_data(self):
        with open("emp.csv") as f:
            return list(csv.DictReader(f))


# ---------- Pipeline ----------
class AutomationPipeline:
    def process(self, adapter, format_name):
        print(f"\n=== Processing {format_name} Data ===")
        records = adapter.get_data()
        for record in records:
            print(record)
        print("Total Records :", len(records))


pipeline = AutomationPipeline()
pipeline.process(JSONAdapter(), "JSON")
pipeline.process(XMLAdapter(), "XML")
pipeline.process(CSVAdapter(), "CSV")
```

### OUTPUT
```text
=== Processing JSON Data ===
{'id': 101, 'name': 'Alice'}
{'id': 102, 'name': 'Bob'}
Total Records : 2

=== Processing XML Data ===
{'id': '201', 'name': 'Charlie'}
{'id': '202', 'name': 'David'}
Total Records : 2

=== Processing CSV Data ===
{'id': '301', 'name': 'Eve'}
{'id': '302', 'name': 'Frank'}
Total Records : 2
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 8: Facade for NLP-Based Customer Support Routing

### AIM
To simplify a multi-layer NLP support-routing framework behind a single Facade interface.

### ALGORITHM
1. Start the

### COMMAND/PROGRAM
No external packages required. Run: `python exp8.py`

```python
class TextPreprocessor:
    def process(self, text):
        return text.lower().strip()


class IntentDetector:
    KEYWORDS = {
        "refund":  "Refund Request",
        "payment": "Billing Issue",
        "login":   "Technical Support",
    }

    def detect(self, text):
        for keyword, intent in self.KEYWORDS.items():
            if keyword in text:
                return intent
        return "General Inquiry"


class SentimentAnalyzer:
    NEGATIVE = ["bad", "angry", "issue", "problem", "not working"]

    def analyze(self, text):
        if any(word in text for word in self.NEGATIVE):
            return "Negative"
        return "Neutral"


class TicketRouter:
    ROUTES = {
        "Refund Request":    "Finance Team",
        "Billing Issue":     "Accounts Team",
        "Technical Support": "IT Support Team",
    }

    def route(self, intent):
        return self.ROUTES.get(intent, "Customer Service Team")


class CustomerSupportFacade:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.detector = IntentDetector()
        self.analyzer = SentimentAnalyzer()
        self.router = TicketRouter()

    def handle_query(self, query):
        text = self.preprocessor.process(query)
        intent = self.detector.detect(text)
        sentiment = self.analyzer.analyze(text)
        department = self.router.route(intent)

        print("\n--- Routing Details ---")
        print("Customer Query :", query)
        print("Intent         :", intent)
        print("Sentiment      :", sentiment)
        print("Route To       :", department)


support = CustomerSupportFacade()
support.handle_query(input("Enter customer query: "))
```

### OUTPUT
```text
Enter customer query: My payment has an issue and I am angry.

--- Routing Details ---
Customer Query : My payment has an issue and I am angry.
Intent         : Billing Issue
Sentiment      : Negative
Route To       : Accounts Team
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 9: Observer-Based Network Anomaly Notification Engine

### AIM
To notify multiple monitoring services automatically when the network anomaly score crosses a threshold.

### ALGORITHM
1. Start the

### COMMAND/PROGRAM
No external packages required. Run: `python exp9.py`

```python
class Observer:
    def update(self, score):
        pass


class AdminAlert(Observer):
    def update(self, score):
        print("Admin Alert: High network anomaly detected! Score =", score)


class FirewallAlert(Observer):
    def update(self, score):
        print("Firewall Alert: Blocking suspicious traffic.")


class LoggingService(Observer):
    def update(self, score):
        print("Logging Service: Incident recorded in security log.")


class NetworkMonitor:
    def __init__(self, threshold=70):
        self.observers = []
        self.threshold = threshold

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, score):
        for observer in self.observers:
            observer.update(score)

    def detect_anomaly(self, score):
        print("\nAnalyzing network traffic...")
        if score >= self.threshold:
            print("Anomaly Threshold Exceeded!")
            self.notify(score)
        else:
            print("Network traffic is normal.")


monitor = NetworkMonitor()
monitor.attach(AdminAlert())
monitor.attach(FirewallAlert())
monitor.attach(LoggingService())

for _ in range(2):
    score = int(input("Enter Network Anomaly Score (0-100): "))
    monitor.detect_anomaly(score)
```

### OUTPUT
```text
Enter Network Anomaly Score (0-100): 85

Analyzing network traffic...
Anomaly Threshold Exceeded!
Admin Alert: High network anomaly detected! Score = 85
Firewall Alert: Blocking suspicious traffic.
Logging Service: Incident recorded in security log.
Enter Network Anomaly Score (0-100): 45

Analyzing network traffic...
Network traffic is normal.
(Loop of 2 runs added so both outcomes are shown.)
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 10: State Pattern for Robotic Picking-Arm Control

### AIM
To control a robotic picking arm with scanning, grasping and docking states using the State pattern.

### ALGORITHM
1. Start the

### COMMAND/PROGRAM
No external packages required. Run: `python exp10.py`

```python
class State:
    def handle(self):
        pass


class ScanningState(State):
    def handle(self):
        print("Robot Arm: Scanning objects...")


class GraspingState(State):
    def handle(self):
        print("Robot Arm: Grasping the detected object...")


class DockingState(State):
    def handle(self):
        print("Robot Arm: Returning to docking station...")


class RobotArm:
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state

    def execute(self):
        self.state.handle()


STATES = {1: ScanningState, 2: GraspingState, 3: DockingState}

print("Select Robot Arm State")
print("1. Scanning")
print("2. Grasping")
print("3. Docking")
choice = int(input("Enter your choice (1-3): "))

if choice in STATES:
    arm = RobotArm()
    arm.set_state(STATES[choice]())
    arm.execute()
else:
    print("Invalid Choice")
```

### OUTPUT
```text
Select Robot Arm State
1. Scanning
2. Grasping
3. Docking
Enter your choice (1-3): 2
Robot Arm: Grasping the detected object...
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 11: Unit Testing with Mocking for Autonomous Decisions

### AIM
To validate an autonomous decision function with unit tests that mock the external weather API.

### ALGORITHM
1. Installtherequired Python libraries.
2. Importtherequired modules.
3. Createafunction to simulate fetching weather information from an external API.
4. Createanautonomous decision function based on the weather data.
5. Writeunittest cases.
6. Use Mocking to replace the real API response.
7. Executealltest cases.
8. Displaythetest results.

### COMMAND/PROGRAM
No external packages required. Run: `python exp11.py`

```python
import unittest
from unittest.mock import patch


def get_weather():
    """Normally this calls a live weather API."""
    return "Sunny"


def decision():
    weather = get_weather()
    if weather == "Sunny":
        return "Go Outside"
    elif weather == "Rainy":
        return "Stay Home"
    return "Unknown Decision"


class TestDecision(unittest.TestCase):

    @patch("__main__.get_weather", return_value="Sunny")
    def test_sunny(self, mock_weather):
        self.assertEqual(decision(), "Go Outside")

    @patch("__main__.get_weather", return_value="Rainy")
    def test_rainy(self, mock_weather):
        self.assertEqual(decision(), "Stay Home")

    @patch("__main__.get_weather", return_value="Cloudy")
    def test_unknown(self, mock_weather):
        self.assertEqual(decision(), "Unknown Decision")


print("Executing Test Cases...\n")
unittest.main(argv=[""], exit=False)
```

### OUTPUT
```text
Executing Test Cases...

...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

### RESULT
The program was executed successfully and the output was verified.


========================================================================


---

## EXP 12: Automated Refactoring of Legacy RPA Workflow

### AIM
To remove duplicated code from a legacy RPA workflow by refactoring it into a reusable function.

### ALGORITHM
1. Import the required Python library.
2. Create a legacy RPA workflow with duplicated code.
3. Execute the legacy workflow.
4. Refactor the duplicated code into a reusable function.
5. Execute the refactored workflow.
6. Compare the outputs of both workflows.
7. Display the improved workflow execution.
8. End the process.

### COMMAND/PROGRAM
No external packages required. Run: `python exp12.py`

```python
import io
import time
from contextlib import redirect_stdout

STEPS = ("Opening Application", "Logging In", "Processing Invoice")


def pause():
    time.sleep(0.2)


# ---------- Legacy workflow (duplicated code) ----------
def legacy_workflow():
    print("Opening Application"); pause()
    print("Logging In"); pause()
    print("Processing Invoice"); pause()

    print("Opening Application"); pause()
    print("Logging In"); pause()
    print("Processing Invoice"); pause()


# ---------- Refactored workflow (reusable function) ----------
def process_invoice():
    for step in STEPS:
        print(step)
        pause()


def refactored_workflow():
    for _ in range(2):
        process_invoice()


def capture(func):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func()
    return buffer.getvalue()


print("=== LEGACY RPA WORKFLOW ===")
legacy_workflow()

print("\n=== REFACTORED RPA WORKFLOW ===")
refactored_workflow()

print("\nOutputs identical:", capture(legacy_workflow) == capture(refactored_workflow))
print("Duplicate code removed; workflow is now reusable and maintainable.")
```

### OUTPUT
```text
=== LEGACY RPA WORKFLOW ===
Opening Application
Logging In
Processing Invoice
Opening Application
Logging In
Processing Invoice

=== REFACTORED RPA WORKFLOW ===
Opening Application
Logging In
Processing Invoice
Opening Application
Logging In
Processing Invoice

Outputs identical: True
Duplicate code removed; workflow is now reusable and maintainable.
```

### RESULT
The program was executed successfully and the output was verified.
