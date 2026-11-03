## EXP 5: UML Sequence and Statechart for Drone Delivery

### AIM
To generate UML Sequence and Statechart diagrams that illustrate the communication flow and operational states of an autonomous drone delivery system.

### ALGORITHM
1. Import the required Python library.
2. Define the sequence diagram participants.
3. Generate the UML Sequence Diagram.
4. Define the states of the drone.
5. Generate the UML Statechart Diagram.
6. Display both diagrams.
7. End the process.

### PROGRAM
```python
from graphviz import Digraph

# Sequence diagram
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

# Statechart diagram
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
```

**SequenceDiagram.png**

![Sequence Diagram](images/SequenceDiagram.png)

**StatechartDiagram.png**

![Statechart Diagram](images/StatechartDiagram.png)

### RESULT
The UML Sequence Diagram and Statechart Diagram for the autonomous drone delivery system were generated successfully.
