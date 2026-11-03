## EXP 10: State Pattern for Robotic Picking-Arm Control

### AIM
To implement the State Design Pattern for a robotic picking-arm controller that enables seamless transitions between scanning, grasping, and docking phases.

### ALGORITHM
1. Start the program.
2. Create a State interface with a handle() method.
3. Implement concrete state classes: ScanningState, GraspingState, DockingState
4. Create a RobotArm context class to maintain the current state.
5. Accept the current operation from the user.
6. Set the corresponding state in the RobotArm.
7. Execute the current state's operation.
8. 
9. Display the robot arm's current activity.
10. Stop the program.
11. 
12. 

### PROGRAM
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
Thus, the State Design Pattern was successfully implemented to control the robotic picking arm by enabling seamless transitions between scanning, grasping, and docking states.
