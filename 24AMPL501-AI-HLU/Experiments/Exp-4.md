# Experiment 4

**Title:** Named Entity Recognition and TF-IDF

## Aim

To write a program to identify named entities and compute TF-IDF scores.

## Algorithm

1. Start
2. Import required libraries.
3. Download necessary NLTK resources.
4. Input the text.
5. Tokenize the text into words.
6. Perform Part-of-Speech (POS) tagging.
7. Apply Named Entity Recognition using ne_chunk().
8. Display the identified named entities.
9. Stop.

## Program

```python
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from sklearn.feature_extraction.text import TfidfVectorizer

text = "Barack Obama was born in Hawaii and worked at Microsoft."
tokens = word_tokenize(text)
pos_tags = pos_tag(tokens)
print("POS Tagged Words:")
print(pos_tags)

print("\nNamed Entities:")
ner_tree = ne_chunk(pos_tags)
print(ner_tree)

documents = [
    "Natural Language Processing is interesting",
    "Machine Learning is a part of Artificial Intelligence",
    "Natural Language Processing uses Machine Learning"
]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()

print("\nTF-IDF Feature Names:")
print(feature_names)
print("\nTF-IDF Matrix:")
print(tfidf_matrix.toarray())
```

## Output

```text
POS Tagged Words:
[('Barack', 'NNP'), ('Obama', 'NNP'), ('was', 'VBD'), ('born', 'VBN'), ('in', 'IN'), ('Hawaii', 'NNP'), ('and', 'CC'), ('worked', 'VBD'), ('at', 'IN'), ('Microsoft', 'NNP'), ('.', '.')]

Named Entities:
(S
  (PERSON Barack/NNP)
  (PERSON Obama/NNP)
  was/VBD
  born/VBN
  in/IN
  (GPE Hawaii/NNP)
  and/CC
  worked/VBD
  at/IN
  (ORGANIZATION Microsoft/NNP)
  ./.)

TF-IDF Feature Names:
['artificial' 'intelligence' 'interesting' 'is' 'language' 'learning'
 'machine' 'natural' 'of' 'part' 'processing' 'uses']

TF-IDF Matrix:
[[0.         0.         0.54935123 0.41779577 0.41779577 0.
  0.         0.41779577 0.         0.         0.41779577 0.        ]
 [0.41756662 0.41756662 0.         0.31757018 0.         0.31757018
  0.31757018 0.         0.41756662 0.41756662 0.         0.        ]
 [0.         0.         0.         0.         0.38550292 0.38550292
  0.38550292 0.38550292 0.         0.         0.38550292 0.50689001]]
```

## Result

Thus, the program was implemented successfully and the output was verified.
