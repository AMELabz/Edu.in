# Experiment 11
**Title:** Spam Filter Using TF-IDF and Naive Bayes

## Aim
To write a Python program that classifies a message as Spam or Ham (not spam) using TF-IDF features and a Multinomial Naive Bayes classifier.

## Algorithm
1. Import pandas and the scikit-learn tools.
2. Create a small dataset of 8 messages with Spam/Ham labels and show it as a DataFrame.
3. Convert the messages to TF-IDF vectors with English stop words removed.
4. Split the data into 75% training and 25% testing.
5. Train a Multinomial Naive Bayes model on the training data.
6. Predict the labels of the test data, then print the accuracy and classification report.
7. Accept a message from the user and convert it to a TF-IDF vector.
8. Predict its class and display SPAM MESSAGE or HAM MESSAGE.

## Program
> `zero_division=0` is added to `classification_report` to remove the long warning that appears in the manual's output.

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

df = pd.DataFrame({
    "message": [
        "Congratulations! You have won a free lottery ticket",
        "Claim your cash prize now",
        "Limited time offer, click here",
        "Meeting scheduled at 10 AM tomorrow",
        "Please submit your assignment today",
        "Let's have lunch together",
        "You won a free vacation package",
        "Your bank account has been credited"],
    "label": ["Spam", "Spam", "Spam", "Ham", "Ham", "Ham", "Spam", "Ham"],
})
print("Dataset Preview:\n", df)

vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(df["message"])
X_train, X_test, y_train, y_test = train_test_split(X, df["label"], test_size=0.25, random_state=42)

model = MultinomialNB().fit(X_train, y_train)
y_pred = model.predict(X_test)
print("\nAccuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

message = input("\nEnter a message to classify:\n")
label = model.predict(vectorizer.transform([message]))[0]
print("\nPrediction:\n" + ("SPAM MESSAGE" if label == "Spam" else "HAM MESSAGE"))
```

## Output
```
Accuracy: 50.0 %

Classification Report:
              precision    recall  f1-score   support
         Ham       0.50      1.00      0.67         1
        Spam       0.00      0.00      0.00         1
    accuracy                           0.50         2
   macro avg       0.25      0.50      0.33         2
weighted avg       0.25      0.50      0.33         2

Enter a message to classify:
Let's have lunch together

Prediction:
HAM MESSAGE
```
*(I ran this code and got the same values as the lab manual.)*

## Result
The Naive Bayes spam filter was trained and tested, and it classified "Let's have lunch together" as HAM MESSAGE. The accuracy is only 50% because the dataset has just 8 messages and the test set has only 2, so a larger dataset is needed for a reliable model.
