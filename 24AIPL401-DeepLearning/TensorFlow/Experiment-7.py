import nltk
import numpy as np
nltk.download('treebank')
from nltk.corpus import treebank
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (Input,Embedding,LSTM,Dense)

# Get tagged sentences
tagged_sentences = treebank.tagged_sents()

print("Number of sentences:", len(tagged_sentences))

# Display first sentence

print(tagged_sentences[0])

#################################################
sentences = []
pos_tags = []

for sentence in treebank.tagged_sents():

    words = []
    tags = []

    for word, tag in sentence:
        words.append(word)
        tags.append(tag)

    sentences.append(words)
    pos_tags.append(tags)

print(sentences[0])
print(pos_tags[0])
print("Number of sentences:", len(sentences[0]))

#################################################
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(
    sentences,
    pos_tags,
    test_size=0.2,
    random_state=42
)

print("Training sentences:", len(X_train))
print("Testing sentences :", len(X_test))
#########################################################
#create Word Tokenizer
word_tokenizer = Tokenizer(
    lower=True,
    oov_token="<UNK>"
)

# Learn vocabulary only from training data
word_tokenizer.fit_on_texts(X_train)

X_train_seq = word_tokenizer.texts_to_sequences(X_train)
X_test_seq = word_tokenizer.texts_to_sequences(X_test)

word_vocab_size = len(word_tokenizer.word_index) + 1

print("\nWord vocabulary size:", word_vocab_size)
#######################################################
#tag Tokenizer
tag_tokenizer = Tokenizer(
    lower=False,
    filters=""
)

tag_tokenizer.fit_on_texts(Y_train)

Y_train_seq = tag_tokenizer.texts_to_sequences(Y_train)
Y_test_seq = tag_tokenizer.texts_to_sequences(Y_test)

tag_vocab_size = len(tag_tokenizer.word_index) + 1

print("POS tag vocabulary size:", tag_vocab_size)

print("\nPOS tag vocabulary:")
print(tag_tokenizer.word_index)
################################################

max_len = max(
    len(sentence)
    for sentence in X_train
)

print("\nMaximum sentence length:", max_len)

############################################
#Padding input tags
X_train_pad = pad_sequences(
    X_train_seq,
    maxlen=max_len,
    padding="post",
    truncating="post"
)

X_test_pad = pad_sequences(
    X_test_seq,
    maxlen=max_len,
    padding="post",
    truncating="post"
)

#Padding POS tags


Y_train_pad = pad_sequences(
    Y_train_seq,
    maxlen=max_len,
    padding="post",
    truncating="post"
)

Y_test_pad = pad_sequences(
    Y_test_seq,
    maxlen=max_len,
    padding="post",
    truncating="post"
)


print("\nInput shape:", X_train_pad.shape)
print("Output shape:", Y_train_pad.shape)
########################################################
# Encoder
encoder_inputs = Input(
    shape=(max_len,),
    name="encoder_input"
)

encoder_embedding = Embedding(
    input_dim=word_vocab_size,
    output_dim=128,
    mask_zero=True,
    name="word_embedding"
)(encoder_inputs)

encoder_lstm = LSTM(
    128,
    return_sequences=True,
    return_state=True,
    name="encoder_lstm"
)

encoder_outputs, state_h, state_c = encoder_lstm(
    encoder_embedding
)

#Decoder
decoder_lstm = LSTM(
    128,
    return_sequences=True,
    return_state=True,
    name="decoder_lstm"
)

decoder_outputs, _, _ = decoder_lstm(
    encoder_outputs,
    initial_state=[state_h, state_c]
)
decoder_dense = Dense(
    tag_vocab_size,
    activation="softmax",
    name="pos_output"
)

outputs = decoder_dense(decoder_outputs)
########################################
model = Model(encoder_inputs,outputs)

model.summary()

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    X_train_pad,
    np.expand_dims(Y_train_pad, axis=-1),
    validation_split=0.1,
    epochs=5,
    batch_size=32,
    verbose=1
)

loss, accuracy = model.evaluate(
    X_test_pad,
    np.expand_dims(Y_test_pad, axis=-1),
    verbose=1
)

print("\nTest Loss:", loss)
print("Test Accuracy:", accuracy)

predictions = model.predict(X_test_pad)

predicted_tag_ids = np.argmax(
    predictions,
    axis=-1
)

id_to_tag = {
    value: key
    for key, value in tag_tokenizer.word_index.items()
}

# Padding index
id_to_tag[0] = "<PAD>"

sample_index = 782

original_words = X_test[sample_index]

actual_tags = Y_test[sample_index]

predicted_tags = []

for i in range(len(original_words)):

    tag_id = predicted_tag_ids[sample_index][i]

    predicted_tags.append(
        id_to_tag.get(tag_id, "UNK")
    )


print("\n====================================")
print("POS TAGGING RESULT")
print("====================================")

print("\nWords:")
print(original_words)

print("\nActual POS Tags:")
print(actual_tags)

print("\nPredicted POS Tags:")
print(predicted_tags)
