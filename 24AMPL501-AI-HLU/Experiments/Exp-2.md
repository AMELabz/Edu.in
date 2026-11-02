# Experiment 2

**Title:** Tokenization, Stopword Removal, Stemming and Lemmatization

## Aim

To write a Python Program to perform preprocessing tasks using NLTK.

## Algorithm

1. Start
2. Import Libraries:
   - nltk
   - word_tokenize, sent_tokenize from nltk.tokenize
   - stopwords from nltk.corpus
   - PorterStemmer, WordNetLemmatizer from nltk.stem
3. Download Required NLTK Resources:
   - punkt (tokenizers)
   - punkt_tab (tokenizer update)
   - stopwords (common stopwords)
   - wordnet (lexical database for lemmatization)
   - omw-1.4 (wordnet data)
4. Input Text:
   - Store the text in a variable text.
5. Sentence Tokenization:
   - Use sent_tokenize(text) to split the text into sentences.
6. Word Tokenization:
   - Use word_tokenize(text) to split the text into individual words.
7. Stopword Removal:
   - Get the set of English stopwords using stopwords.words('english').
   - Remove words from the token list that appear in the stopword set.
8. Stemming:
   - Initialize PorterStemmer().
   - Apply the stemmer to each word in the filtered list.
9. Lemmatization:
   - Initialize WordNetLemmatizer().
10. Apply the lemmatizer to each word in the filtered list.
11. Display Results:
12. Print sentence tokens, word tokens, words after stopword removal, stemmed words and lemmatized words
13. Stop

## Program

```python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

text = """
Natural Language Processing is a branch of Artificial Intelligence.
It enables computers to understand human language and process text efficiently.
"""

sentences = sent_tokenize(text)
print(sentences)

words = word_tokenize(text)
print(words)

stop_words = set(stopwords.words('english'))
filtered_words = [word for word in words if word.lower() not in stop_words]
print(filtered_words)

stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in filtered_words]
print(stemmed_words)

lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

print(lemmatized_words)
```

## Output

```text
Sentence Tokens:
['\nNatural Language Processing is a branch of Artificial Intelligence.', 'It enables computers to understand human language and process text efficiently.']

Word Tokens:
['Natural', 'Language', 'Processing', 'is', 'a', 'branch', 'of', 'Artificial', 'Intelligence', '.', 'It', 'enables', 'computers', 'to', 'understand', 'human', 'language', 'and', 'process', 'text', 'efficiently', '.']

Words After Stopword Removal:
['Natural', 'Language', 'Processing', 'branch', 'Artificial', 'Intelligence', '.', 'enables', 'computers', 'understand', 'human', 'language', 'process', 'text', 'efficiently', '.']

Stemmed Words:
['natur', 'languag', 'process', 'branch', 'artifici', 'intellig', '.', 'enabl', 'comput', 'understand', 'human', 'languag', 'process', 'text', 'effici', '.']

Lemmatized Words:
['Natural', 'Language', 'Processing', 'branch', 'Artificial', 'Intelligence', '.', 'enables', 'computer', 'understand', 'human', 'language', 'process', 'text', 'efficiently', '.']
```

## Result

Thus, the program was implemented successfully and the output was verified.
