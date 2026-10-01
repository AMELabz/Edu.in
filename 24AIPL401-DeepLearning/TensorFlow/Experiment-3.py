# ## Aim
# To build and train a CNN using TensorFlow and Keras for handwritten character classification
# on the EMNIST Balanced dataset, and evaluate its performance using accuracy, loss curves,
# and sample predictions.

# ## Algorithm
# 1. Import required libraries — idx2numpy, NumPy, Matplotlib, TensorFlow, Keras layers.
# 2. Load EMNIST Balanced dataset, normalize pixel values, and reshape images with channel dimension.
# 3. Build a Sequential CNN with Conv2D + MaxPooling blocks, Flatten, Dense, and Dropout layers.
# 4. Compile the model with Adam optimizer and sparse categorical cross-entropy loss.
# 5. Train the model with a validation split for multiple epochs.
# 6. Evaluate the model on the test dataset to get loss and accuracy.
# 7. Plot training and validation accuracy/loss curves.
# 8. Predict a sample image's character using the mapping file and display the result with confidence.

# ## Result
# The CNN model was successfully trained on the EMNIST Balanced dataset and achieved good
# accuracy in classifying handwritten characters across 47 classes, with the loss and accuracy
# curves confirming effective learning.

import gzip
import idx2numpy
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Extract .gz files
files = [
    "emnist-balanced-train-images-idx3-ubyte.gz",
    "emnist-balanced-train-labels-idx1-ubyte.gz",
    "emnist-balanced-test-images-idx3-ubyte.gz",
    "emnist-balanced-test-labels-idx1-ubyte.gz"
]

for f in files:
    with gzip.open(f, "rb") as src, open(f[:-3], "wb") as dst:
        dst.write(src.read())

# Load EMNIST dataset
x_train = idx2numpy.convert_from_file("emnist-balanced-train-images-idx3-ubyte")
y_train = idx2numpy.convert_from_file("emnist-balanced-train-labels-idx1-ubyte")
x_test = idx2numpy.convert_from_file("emnist-balanced-test-images-idx3-ubyte")
y_test = idx2numpy.convert_from_file("emnist-balanced-test-labels-idx1-ubyte")

print("Training Images :", x_train.shape)
print("Training Labels :", y_train.shape)
print("Testing Images  :", x_test.shape)
print("Testing Labels  :", y_test.shape)

# Normalize and reshape
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

print(x_train.shape)
print(x_test.shape)

print("Classes:", np.unique(y_train))
print("Number of classes:", len(np.unique(y_train)))

# Build CNN
model = Sequential([
    Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation="relu"),
    Dropout(0.5),
    Dense(47, activation="softmax")
])

# Compile
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Train
history = model.fit(
    x_train,
    y_train,
    epochs=4,
    batch_size=64,
    validation_split=0.2
)

# Evaluate
test_loss, test_accuracy = model.evaluate(x_test, y_test)

print("\nTest Loss :", test_loss)
print("Test Accuracy :", test_accuracy)

# Plot Accuracy and Loss
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
plt.title("Accuracy Curve")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.title("Loss Curve")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.tight_layout()
plt.show()

# Character mapping
mapping = {}

with open("emnist-balanced-mapping.txt") as f:
    for line in f:
        label, ascii_code = line.split()
        mapping[int(label)] = chr(int(ascii_code))

# Select image
index = 25
image = x_test[index]
label = y_test[index]

plt.imshow(image.reshape(28, 28), cmap="gray")
plt.axis("off")
plt.show()

# Predict
prediction = model.predict(np.expand_dims(image, axis=0))
predicted_label = np.argmax(prediction)

print("Actual Character   :", mapping[label])
print("Predicted Character:", mapping[predicted_label])
print("Confidence         :", round(np.max(prediction) * 100, 2), "%")