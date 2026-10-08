# Experiment 10
**Title:** Next Word Prediction

## Aim
To write a Python program that predicts the next word after a given word, using bigrams built from a text corpus.

## Algorithm
1. Import NLTK, `defaultdict` and `Counter`, and download the `punkt` and `punkt_tab` tokenizer data.
2. Define the sample text corpus.
3. Convert the corpus to lowercase and split it into word tokens.
4. Generate all bigram pairs (word, next word) from the tokens.
5. For each pair, store the second word in a dictionary under the first word.
6. Accept an input word from the user and convert it to lowercase.
7. If the word is in the dictionary, show all possible next words and pick the most frequent one as the prediction.
8. If the word is not in the dictionary, display "Word not found in corpus".

## Program
```python
import nltk
from collections import Counter, defaultdict

nltk.download("punkt")
nltk.download("punkt_tab")

corpus = """
Natural Language Processing is an important field of Artificial Intelligence.
Natural Language Processing enables computers to understand human language.
Artificial Intelligence and Machine Learning are transforming technology.
Machine Learning is a subset of Artificial Intelligence.
"""

tokens = nltk.word_tokenize(corpus.lower())
next_words = defaultdict(list)                  # word -> every word that follows it
for first, second in nltk.bigrams(tokens):
    next_words[first].append(second)

word = input("Enter a word: ").lower()
if word in next_words:
    options = next_words[word]
    print("\nPossible Next Words:\n", options)
    print("\nPredicted Next Word:\n", Counter(options).most_common(1)[0][0])
else:
    print("\nWord not found in corpus.")
```

## Output
```
Enter a word: transforming
Possible Next Words:
['technology']
Predicted Next Word:
technology

Enter a word: is
Possible Next Words:
['an', 'a']
Predicted Next Word:
an
```
*(From the lab manual run. I checked the bigram logic on my side and got the same two results.)*

## Result
The bigram model predicted the next word correctly. After "transforming" it predicted "technology", and after "is" it predicted "an" (the first of the equally frequent choices "an" and "a").
