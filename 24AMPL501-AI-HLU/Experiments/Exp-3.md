# Experiment 3

**Title:** POS Tagging and Chunking

## Aim

To write a Python Porgam to identify grammatical categories and phrase structures.

## Algorithm

1. Start
2. Import the required NLTK libraries and download the necessary resources (punkt, punkt_tab, averaged_perceptron_tagger, averaged_perceptron_tagger_eng).
3. Store the input sentence in a variable.
4. Tokenize the sentence into words using word_tokenize().
5. Perform Part-of-Speech (POS) tagging on the tokenized words using pos_tag().
6. Define the chunk grammar for noun phrases:
   - NP: {<DT>?<JJ>*<NN>}
7. Create a chunk parser using RegexpParser() with the defined grammar.
8. Parse the POS-tagged words to generate a chunk tree.
9. Display the POS tags and chunk tree.
10. Traverse the chunk tree and identify subtrees labeled NP.
11. Extract and print the noun phrases from the identified chunks.
12. Stop.

## Program

```python
import nltk
from nltk import word_tokenize, pos_tag
from nltk.chunk import RegexpParser

sentence = "The little cat sat on the red mat"

words = word_tokenize(sentence)
words

pos_tags = pos_tag(words)
print("POS Tags:")
print(pos_tags)

grammar = r"""
NP: {<DT>?<JJ>*<NN>}
"""

chunk_parser = RegexpParser(grammar)

chunk_tree = chunk_parser.parse(pos_tags)
print("\nChunk Tree:")
print(chunk_tree)

print("\nNoun Phrases:")
for subtree in chunk_tree.subtrees():
    if subtree.label() == 'NP':
        print(" ".join(word for word, tag in subtree.leaves()))
```

## Output

```text
POS Tags:
[('The', 'DT'), ('little', 'JJ'), ('cat', 'NN'), ('sat', 'VBD'), ('on', 'IN'), ('the', 'DT'), ('red', 'JJ'), ('mat', 'NN')]

Chunk Tree:
(S
  (NP The/DT little/JJ cat/NN)
  sat/VBD
  on/IN
  (NP the/DT red/JJ mat/NN))

Noun Phrases:
The little cat
the red mat
```

## Result

Thus, the program, was implemented successfully and the output was verified.
