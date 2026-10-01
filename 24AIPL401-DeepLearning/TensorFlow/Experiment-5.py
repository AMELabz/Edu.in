# EXPERIMENT 5 – CHARACTER LEVEL TEXT GENERATION USING RNN

# AIM
# To develop a character-level text generation model using a Simple Recurrent Neural Network (SimpleRNN) with
# TensorFlow and generate Shakespeare-style text from a given text corpus.

# ALGORITHM
# 1. Import TensorFlow and NumPy libraries.
# 2. Load the Shakespeare text corpus from the given text file and display its basic information.
# 3. Create a character vocabulary by finding all unique characters and assign an integer index to each character.
# 4. Convert the complete text corpus from characters into their corresponding integer representations.
# 5. Create input and target sequences of length 100, where the target sequence is shifted by one character.
# 6. Convert the sequences into a TensorFlow dataset, shuffle them, and divide them into batches of 64.
# 7. Build a Sequential model containing an Embedding layer, a SimpleRNN layer with 256 units, and a Dense output layer
#    with 65 classes; compile and train it for one epoch.
# 8. Generate new text by predicting one character at a time from the starting text “Shall ” using the trained RNN.

# OUTPUT
# The corpus was loaded successfully and the character-level RNN model was trained for one epoch.
# New Shakespeare-style text was generated starting from “Shall ”.

# RESULT
# Thus, a character-level text generation model using an Embedding layer, SimpleRNN, and Dense layer was successfully
# implemented. The Shakespeare corpus was converted into character sequences, used to train the RNN for one epoch,
# and the trained model was used to generate new text beginning with “Shall ”.

import tensorflow as tf
import numpy as np

file_path = r"C:\Users\sathi\OneDrive\Documents\dl\dl\Exp_5\shakespeare.txt"

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

print("Corpus loaded successfully.")
print("Corpus length:", len(text))
print(text)
print("\nFirst 10 characters:")
print(text[:10])

vocab = sorted(set(text))
vocab_size = len(vocab)

char_to_int = {char: i for i, char in enumerate(vocab)}
print(char_to_int)
print("Vocabulary size:", vocab_size)

text_as_int = np.array([char_to_int[char] for char in text])
print("Sample text:", text[:5])
print("Integer representation:", text_as_int[:5])

sequence_length = 100
X = []
Y = []

for i in range(len(text_as_int) - sequence_length):
    X.append(text_as_int[i:i + sequence_length])
    Y.append(text_as_int[i + 1:i + sequence_length + 1])

X = np.array(X)
Y = np.array(Y)

print("Input shape:", X.shape)
print("Target shape:", Y.shape)

batch_size = 64
dataset = tf.data.Dataset.from_tensor_slices((X, Y))
dataset = dataset.shuffle(10000).batch(batch_size, drop_remainder=True)

print("Dataset created successfully")
print("Batch size:", batch_size)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=65, output_dim=128),
    tf.keras.layers.SimpleRNN(256, return_sequences=True),
    tf.keras.layers.Dense(65)
])

model.summary()

loss_function = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer="adam", loss=loss_function)
history = model.fit(dataset, epochs=1)

int_to_char = {i: char for i, char in enumerate(vocab)}

def generate_text(start_text, length=200):
    result = start_text

    for i in range(length):
        x = [char_to_int[c] for c in result[-100:]]
        x = np.array([x])
        prediction = model.predict(x, verbose=0)
        next_id = np.argmax(prediction[0, -1])
        next_char = int_to_char[next_id]
        result += next_char

    return result

text = generate_text("Shall ", 200)

print("\nGenerated Text:")
print(text)