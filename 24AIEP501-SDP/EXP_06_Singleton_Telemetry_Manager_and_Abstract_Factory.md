## EXP 6: Singleton Telemetry Manager and Abstract Factory

### AIM
To implement a thread-safe Singleton Telemetry Manager and an Abstract Factory Pattern for creating Web, Desktop, and Mobile automation drivers dynamically.

### ALGORITHM
1. Import the required library.
2. Create a Thread-safe Singleton Telemetry Manager.
3. Define Web, Desktop, and Mobile driver classes.
4. Create an Abstract Factory.
5. Instantiate different drivers using the factory.
6. Display the created drivers.
7. End the process.

### PROGRAM
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
The thread-safe Singleton Telemetry Manager and Abstract Factory Pattern were implemented successfully, enabling runtime creation of Web, Desktop, and Mobile UI automation drivers.
