# Experiment 6

**Title:** Write a Python program to train CBOW and Skip-gram Word2Vec
models on a given text corpus.

## Aim

To write a Python program to train Word2Vec models and analyze word
relationships.

## Algorithm

1.  Install and import the required libraries: gensim, scikit-learn and
    matplotlib.
2.  Create a sample text corpus consisting of multiple sentences.
3.  Train a Word2Vec model using the CBOW architecture (`sg=0`).
4.  Train another Word2Vec model using the Skip-Gram architecture
    (`sg=1`).
5.  Find words similar to the target word `"machine"` using both models.
6.  Extract the vocabulary and corresponding word vectors from the
    Skip-Gram model.
7.  Apply PCA to reduce the word-vector dimensions from 50 to 2.
8.  Plot and label the reduced word embeddings.
9.  Display the similar words and embedding visualization.

## Program

``` python
# pip install gensim

from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

corpus = [
    ["natural", "language", "processing", "is", "interesting"],
    ["machine", "learning", "is", "a", "part", "of", "artificial", "intelligence"],
    ["deep", "learning", "improves", "machine", "learning"],
    ["natural", "language", "processing", "uses", "machine", "learning"],
    ["artificial", "intelligence", "includes", "machine", "learning"],
    ["cats", "and", "dogs", "are", "pets"],
    ["dog", "is", "a", "faithful", "animal"],
    ["cat", "is", "a", "cute", "animal"]
]

cbow = Word2Vec(corpus, vector_size=50, window=3, min_count=1, sg=0)
skipgram = Word2Vec(corpus, vector_size=50, window=3, min_count=1, sg=1)

print("CBOW:", cbow.wv.most_similar("machine"))
print("Skip-Gram:", skipgram.wv.most_similar("machine"))

words = skipgram.wv.index_to_key
vectors = [skipgram.wv[w] for w in words]
points = PCA(n_components=2).fit_transform(vectors)

plt.figure(figsize=(8, 6))
plt.scatter(points[:, 0], points[:, 1])
for i, word in enumerate(words):
    plt.annotate(word, points[i])
plt.title("Word2Vec Embeddings (Skip-Gram)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.show()
```

## Output

``` text
CBOW - Similar words to 'machine':
[('dogs', ...), ('interesting', ...), ('includes', ...), ...]

Skip-Gram - Similar words to 'machine':
[('dogs', ...), ('interesting', ...), ('includes', ...), ...]
```

The program also displays a 2D PCA visualization of the Skip-Gram word
embeddings.

## Result

Thus, the CBOW and Skip-Gram Word2Vec models were successfully trained
on the given text corpus. The models successfully identified similar
words and visualized the learned word embeddings.
