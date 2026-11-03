## EXP 4: Polymorphic Sensor Hardware Wrapper

### AIM
To develop an object-oriented abstract hardware wrapper layer using polymorphism to process inputs from different sensor types dynamically.

### ALGORITHM
1. Import the Abstract Base Class module.
2. Create an abstract class named Sensor.
3. Define an abstract method read_data().
4. Create subclasses for Temperature, Humidity and Motion sensors.
5. Override the read_data() method in each subclass.
6. Store all sensor objects in a list.
7. Access every sensor through the base class reference.
8. Display the sensor values using polymorphism.
9. End the program.

### PROGRAM
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
Temperature : 30 C
Humidity    : 45 %
Motion      : Detected
```

*Sensor values are random, so they change on every run.*

### RESULT
Thus, an object-oriented abstract hardware wrapper layer was successfully developed using polymorphism to process inputs from multiple sensor types dynamically.
