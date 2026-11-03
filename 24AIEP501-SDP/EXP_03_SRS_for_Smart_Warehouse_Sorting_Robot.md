## EXP 3: SRS for Smart Warehouse Sorting Robot

### AIM
To draft a Software Requirement Specification (SRS) for a Smart Warehouse Sorting Robot that identifies system requirements and maps multi-threaded failure modes for reliable and efficient warehouse automation.

### ALGORITHM
1. Identify the stakeholders of the warehouse sorting system.
2. Define the functional requirements of the robot.
3. Define non-functional requirements such as performance, reliability, safety and scalability.
4. Identify the different threads running simultaneously in the robot.
5. Analyze possible failure modes for each thread.
6. Document the mitigation strategy for every failure.
7. Prepare the Software Requirement Specification (SRS).
8. Verify the completeness of the SRS.
9. End the process.

### PROGRAM
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
    "Sensor Thread":   ("Sensor Failure",           "Restart Sensor"),
    "Camera Thread":   ("Image Capture Failure",    "Capture Again"),
    "Barcode Thread":  ("Barcode Not Detected",     "Manual Verification"),
    "Sorting Thread":  ("Mechanical Jam",           "Stop Conveyor and Alert Operator"),
    "Database Thread": ("Database Connection Lost", "Reconnect Database"),
    "Network Thread":  ("Communication Failure",    "Retry Network Connection"),
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
Thus, the Software Requirement Specification for the Smart Warehouse Sorting Robot was successfully drafted, and the multi-threaded failure modes with suitable mitigation strategies were identified.
