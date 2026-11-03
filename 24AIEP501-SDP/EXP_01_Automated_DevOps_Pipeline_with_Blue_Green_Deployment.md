## EXP 1: Automated DevOps Pipeline with Blue-Green Deployment

### AIM
To build an automated DevOps pipeline for an Intelligent Document Processing (IDP) scoring model using Blue-Green deployment, allowing easy model deployment, traffic switching, and rollback.

### ALGORITHM
1. Install the required Python libraries.
2. Create an IDP dataset with the following features: Pages, Words, Images, Tables, Score
3. Train the Blue Model using the dataset.
4. Save the Blue model as model_blue.pkl.
5. Create a modified dataset and train the Green Model.
6. Save the Green model as model_green.pkl.
7. Load both models and set Blue as the active deployment.
8. Predict the document score using the active model.
9. Switch the deployment from Blue to Green.
10. Predict the document score using the Green model.
11. If the Green model has any issue, switch back (rollback) to the Blue model.
12. End the process.

### PROGRAM
```python
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# Create IDP dataset
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

# Train and save BLUE model
blue = LinearRegression().fit(data[FEATURES], data["Score"])
joblib.dump(blue, "model_blue.pkl")

# Train and save GREEN model (modified data)
data_green = data.copy()
data_green["Words"] *= 1.02
green = LinearRegression().fit(data_green[FEATURES], data_green["Score"])
joblib.dump(green, "model_green.pkl")

# Deploy
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
The DevOps pipeline was successfully created using Blue-Green deployment. It enabled easy model deployment, traffic switching, and quick rollback when required.
