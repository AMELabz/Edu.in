# Experiment 1

**Title:** N-grams and Bigram Model with Add-One Smoothing

## Aim

To write a Python Program to generate unigrams, bigrams and trigrams and compute sentence probability using a bigram model.

## Algorithm

1. Start
2. Import the required NLTK libraries:
   - nltk
   - ngrams from nltk.util
   - word_tokenize from nltk.tokenize
3. Download the required tokenizer resources:
   - punkt
   - punkt_tab
4. Store the input sentence in a variable text.
5. Convert the text to lowercase using text.lower().
6. Tokenize the text into individual words using word_tokenize().
7. Generate unigrams by creating 1-word sequences from the token list using ngrams(tokens, 1).
8. Generate bigrams by creating 2-word sequences from the token list using ngrams(tokens, 2).
9. Generate trigrams by creating 3-word sequences from the token list using ngrams(tokens, 3).
10. Convert the generated n-grams into lists.
11. Display the unigrams, bigrams and trigrams
12. Stop

## Program

```python
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize

text = 'this is my cat this is my dog'
tokens = word_tokenize(text.lower())
tokens

print("Unigrams:", list(ngrams(tokens, 1)))
print("Bigrams:", list(ngrams(tokens, 2)))
print("Trigrams:", list(ngrams(tokens, 3)))

import math
from collections import Counter

corpus = "this is my cat this is my dog i love my cat"
tokens = word_tokenize(corpus.lower())
V = len(set(tokens))
uni = Counter(ngrams(tokens, 1))
bi = Counter(ngrams(tokens, 2))

test = "this is my frog"  # 'frog' is unseen
test_bi = list(ngrams(word_tokenize(test.lower()), 2))
test_bi

prob = 1.0
for w1, w2 in test_bi:
    c_bi = bi.get((w1, w2), 0)
    c_uni = uni.get((w1,), 0)
    # Formula: P = (C(w1,w2) + 1) / (C(w1) + V)
    prob *= (c_bi + 1) / (c_uni + V)

print(f"Sentence Probability: {prob:.6f}")
```

## Output

```text
Unigrams: [('this',), ('is',), ('my',), ('cat',), ('this',), ('is',), ('my',), ('dog',)]
Bigrams: [('this', 'is'), ('is', 'my'), ('my', 'cat'), ('cat', 'this'), ('this', 'is'), ('is', 'my'), ('my', 'dog')]
Trigrams: [('this', 'is', 'my'), ('is', 'my', 'cat'), ('my', 'cat', 'this'), ('cat', 'this', 'is'), ('this', 'is', 'my'), ('is', 'my', 'dog')]

Sentence Probability: 0.011111
```

## Result

Thus, the program was implemented successfully and the output was verified.
