import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

print("TensorFlow version:", tf.__version__)
print("NumPy version:", np.__version__)

# Load and preprocess data
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)
x_train = pad_sequences(x_train, maxlen=200)
x_test = pad_sequences(x_test, maxlen=200)

# Build LSTM model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(10000, 128),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

# Train model
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.fit(x_train, y_train, epochs=3, batch_size=64)

# Test model accuracy
loss, accuracy = model.evaluate(x_test, y_test)
print("Test Accuracy:", accuracy)

# Test a custom sentence
word_index = imdb.get_word_index()

sentence = "This movie was super"

encoded = [
    word_index.get(word.lower(), 2) + 3
    for word in sentence.split()
]

encoded = pad_sequences([encoded], maxlen=200)

prediction = model.predict(encoded)[0][0]

print("\nSentence:", sentence)
print("Sentiment:", "Positive" if prediction >= 0.5 else "Negative")
print("Prediction Score:", prediction)
