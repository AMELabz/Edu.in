# Aim :

# To build and train an Artificial Neural Network (ANN) using TensorFlow and Keras for handwritten digit classification on the MNIST dataset.
# To evaluate the model's performance using accuracy, loss, and training-validation curves.

# Algorithm :

# 1. Import the required TensorFlow, Keras, and Matplotlib libraries.
# 2. Load the MNIST dataset and normalize the pixel values.
# 3. Create a Sequential ANN model with a Flatten layer, one hidden Dense layer, and an output Dense layer.
# 4. Compile the model using the Adam optimizer and sparse categorical cross-entropy loss function.
# 5. Train the model using the training dataset with validation data for multiple epochs.
# 6. Evaluate the trained model on the test dataset to obtain loss and accuracy.
# 7. Plot the training and validation loss curves.
# 8. Plot the training and validation accuracy curves and analyze the model performance.


# Result:

# The ANN model was successfully trained on the MNIST dataset and achieved high accuracy in handwritten digit classification. The loss and accuracy curves indicated effective learning and good model performance.


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = x_train / 255.0
x_test = x_test / 255.0

model = Sequential([
    Flatten(input_shape=(28, 28)),     # Convert 28x28 image into 784 features
    Dense(64, activation='relu'),     # Hidden layer
    #Dense(64, activation='relu'), 
    Dense(10, activation='softmax')    # Output layer (10 classes)
])

model.summary()

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

history = model.fit(
    x_train,
    y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

print(f"\nTest Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

# Plot Loss Curve
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title("Loss Curve")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

# Plot Accuracy Curve
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title("Accuracy Curve")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.tight_layout()
plt.show()
