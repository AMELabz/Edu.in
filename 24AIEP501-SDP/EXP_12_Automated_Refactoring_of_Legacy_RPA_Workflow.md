## EXP 12: Automated Refactoring of Legacy RPA Workflow

### AIM
To execute an automated structural code refactoring process that removes duplicated code and improves the maintainability and operational throughput of a legacy RPA workflow.

### ALGORITHM
1. Import the required Python library.
2. Create a legacy RPA workflow with duplicated code.
3. Execute the legacy workflow.
4. Refactor the duplicated code into a reusable function.
5. Execute the refactored workflow.
6. Compare the outputs of both workflows.
7. Display the improved workflow execution.
8. End the process.

### PROGRAM
```python
import io
import time
from contextlib import redirect_stdout

STEPS = ("Opening Application", "Logging In", "Processing Invoice")


def pause():
    time.sleep(0.2)


# Legacy workflow (duplicated code)
def legacy_workflow():
    print("Opening Application"); pause()
    print("Logging In"); pause()
    print("Processing Invoice"); pause()

    print("Opening Application"); pause()
    print("Logging In"); pause()
    print("Processing Invoice"); pause()


# Refactored workflow (reusable function)
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
The automated structural code refactoring was executed successfully by eliminating duplicate code and improving the maintainability of the legacy RPA workflow.
