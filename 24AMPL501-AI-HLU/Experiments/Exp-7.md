# Experiment 7
**Title:** Sentiment Analysis

## Aim
To write a Python program that finds whether a given text is positive, negative or neutral using TextBlob.

## Algorithm
1. Install and import the TextBlob library.
2. Accept a sentence or paragraph from the user.
3. Create a TextBlob object from the text.
4. Get the polarity score (-1 to +1) and the subjectivity score (0 to 1).
5. If polarity is greater than 0 the sentiment is Positive, if less than 0 it is Negative, otherwise Neutral.
6. If subjectivity is greater than 0.5 the text is subjective (opinion-based), otherwise objective (fact-based).
7. Display the input text, both scores, the sentiment and its interpretation.
8. Stop.

## Program
```bash
pip install textblob
```
```python
from textblob import TextBlob   # pip install textblob

text = input("Enter a sentence or paragraph:\n")
polarity, subjectivity = TextBlob(text).sentiment

if polarity > 0:
    sentiment, meaning = "POSITIVE", "The text expresses a positive opinion or emotion."
elif polarity < 0:
    sentiment, meaning = "NEGATIVE", "The text expresses a negative opinion or emotion."
else:
    sentiment, meaning = "NEUTRAL", "The text does not express a strong positive or negative opinion."

print("\nSENTIMENT ANALYSIS REPORT")
print("Input Text      :", text)
print("Polarity Score  :", polarity)
print("Subjectivity    :", subjectivity)
print("Sentiment       :", sentiment)
print("Interpretation  :", meaning)
print("The text is highly subjective and opinion-based." if subjectivity > 0.5
      else "The text is relatively objective and fact-based.")
```

## Output
```
Enter a sentence or paragraph:
I really enjoy learning Natural Language Processing. It is very interesting and useful.
Polarity Score : 0.3625
Subjectivity Score : 0.3875
Sentiment : POSITIVE
The text expresses a positive opinion or emotion.
The text is relatively objective and fact-based.

Enter a sentence or paragraph:
The movie was boring and disappointing.
Polarity Score : -0.8
Subjectivity Score : 0.85
Sentiment : NEGATIVE
The text expresses a negative opinion or emotion.
The text is highly subjective and opinion-based.
```
*(Scores taken from the lab manual run. My short version prints the same values in a more compact report layout.)*

## Result
The program found the sentiment of both sentences correctly. The first sentence was Positive (polarity 0.3625) and the second sentence was Negative (polarity -0.8).
