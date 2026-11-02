# Experiment 5

**Title:** CYK Parsing / Chart Parsing

## Aim

To write a Python program to parse sentences using context-free grammar.

## Algorithm

1. Start.
2. Import the required NLTK modules (CFG and ChartParser).
3. Define the Context-Free Grammar (CFG) with production rules.
4. Create a Chart Parser using the defined grammar.
5. Input the sentence to be parsed.
6. Tokenize the sentence into individual words.
7. Display the input sentence.
8. Pass the tokenized words to the parser.
9. Generate parse trees based on the grammar rules.
10. Display all valid parse trees.
11. Stop.

## Program

```python
import nltk
from nltk import CFG
from nltk.parse import ChartParser

grammar = CFG.fromstring("""
S -> NP VP
NP -> Det N
VP -> V NP
Det -> 'the'
N -> 'cat' | 'dog'
V -> 'chased' | 'saw'
""")

grammar

parser = ChartParser(grammar)
print(parser)

sentence = "the cat chased the dog"
words = sentence.split()

print("Input Sentence:",sentence)

print("\nParse Trees:")
for tree in parser.parse(words):
    print(tree)
```

## Output

```text
Input Sentence:
the cat chased the dog

Parse Trees:
(S (NP (Det the) (N cat)) (VP (V chased) (NP (Det the) (N dog))))
```

## Result

Thus, the program was implemented successfully and the output was verified.
