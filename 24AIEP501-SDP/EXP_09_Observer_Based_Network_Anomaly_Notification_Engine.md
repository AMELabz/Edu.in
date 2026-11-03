## EXP 9: Observer-Based Network Anomaly Notification Engine

### AIM
To implement the Observer Design Pattern for a network anomaly detection system that automatically notifies multiple monitoring services whenever the anomaly level exceeds predefined thresholds.

### ALGORITHM
1. Start the program.
2. Create an Observer interface with an update() method.
3. Create concrete observer classes such as AdminAlert, FirewallAlert, and
4. LoggingService.
5. Create a NetworkMonitor (Subject) class.
6. Register observers with the NetworkMonitor.
7. Accept the network anomaly score from the user.
8. Compare the score with the threshold value.
9. If the threshold is exceeded, notify all registered observers.
10. Display the corresponding alert messages.
11. Stop the program.

### PROGRAM
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
```

*The loop runs twice so both outcomes (threshold exceeded and normal) are shown.*

### RESULT
Thus, the Observer Design Pattern was successfully implemented to trigger real-time notifications whenever the network anomaly detection threshold was exceeded, enabling automatic alerts to multiple monitoring services.
