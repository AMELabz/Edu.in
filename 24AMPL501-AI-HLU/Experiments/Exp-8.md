# Experiment 8
**Title:** Fake News Detection Using TF-IDF and Logistic Regression

## Aim
To write a Python program that classifies a news article as Real or Fake using TF-IDF features and Logistic Regression.

## Algorithm
1. Import pandas and the scikit-learn tools, then read the CSV dataset path from the user.
2. Load the dataset and check that it has the `text` and `label` columns.
3. Split the data into 80% training and 20% testing.
4. Convert the text to TF-IDF vectors (English stop words removed, `max_df=0.7`), learning the vocabulary from the training text only.
5. Train a Logistic Regression model on the training vectors.
6. Predict the labels of the test data, then print the accuracy and the classification report.
7. Ask the user for a news article and convert it to a TF-IDF vector (stop when the user types `exit`).
8. Predict and display FAKE NEWS or REAL NEWS, and repeat until the user types `exit`.

## Program
> **FIX vs. the lab manual:** the manual fits TF-IDF on the whole dataset before splitting, so test-data words leak into training. Here the split is done first.

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

df = pd.read_csv(input("Enter the path of the CSV dataset: "))
print("\nDataset Preview:\n", df.head())
if not {"text", "label"} <= set(df.columns):
    raise SystemExit("Dataset must contain 'text' and 'label' columns.")

# FIX: split first, then fit TF-IDF on training data only (no test-data leakage)
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
model = LogisticRegression(max_iter=1000).fit(vectorizer.fit_transform(X_train), y_train)

y_pred = model.predict(vectorizer.transform(X_test))
print("\nModel Accuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

while True:
    news = input("\nEnter a news article to check (or type 'exit'): ")
    if news.lower() == "exit":
        break
    label = model.predict(vectorizer.transform([news]))[0]
    print("Prediction:", "FAKE NEWS" if str(label).upper() == "FAKE" else "REAL NEWS")
```

## Output
Your lab manual has no output for this experiment. Run the program on your own dataset (a CSV with columns `text` and `label`, where label is `FAKE` or `REAL`) and paste the real output here:

```
Model Accuracy: ____ %
Classification Report: (precision, recall, f1-score table)
Enter a news article to check (or type 'exit'): ...
Prediction: FAKE NEWS / REAL NEWS
```
I tested the code only on a 12-row demo file, so its accuracy there means nothing for your record.

## Result
The Logistic Regression model was trained on TF-IDF features of the news dataset. It reported its accuracy and classification report on the test data, and it classified user-entered articles as FAKE NEWS or REAL NEWS. *(Add your accuracy value from your run.)*
