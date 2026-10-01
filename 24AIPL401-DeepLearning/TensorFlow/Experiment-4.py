# AIM :
# To develop a Convolutional Neural Network (CNN) model using TensorFlow to recognize and classify
# different persons from facial images in the LFW (Labeled Faces in the Wild) dataset.

# ALGORITHM
# 1. Import NumPy, TensorFlow, Matplotlib, and Scikit-learn libraries.
# 2. Load the LFW face dataset with a minimum of 70 images per person.
# 3. Extract the face images and corresponding target labels.
# 4. Normalize the image pixel values and add the channel dimension.
# 5. Split the dataset into 80% training data and 20% testing data using stratified sampling.
# 6. Build a CNN using Conv2D, ReLU, MaxPooling, Flatten, and Dense layers.
# 7. Compile the model using Adam optimizer and sparse categorical cross-entropy loss, then train it for 10 epochs.
# 8. Evaluate the trained model on the test data and predict the identity of a sample test face.

# RESULT
# Thus, a CNN-based face recognition model was successfully implemented using the LFW dataset.
# The trained model was evaluated on the test dataset and used to predict the identity of a sample facial image.

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

lfw = fetch_lfw_people(min_faces_per_person=70, resize=0.5, color=False)

for i, name in enumerate(lfw.target_names):
    count = np.sum(lfw.target == i)
    print(name, ":", count, "images")

print("\nTotal images:", len(lfw.images))
print("Total people:", len(lfw.target_names))

X = lfw.images
y = lfw.target
X = X / 255.0
X = np.expand_dims(X, axis=-1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\nTraining images:", len(X_train))
print("Testing images:", len(X_test))

model = Sequential([
    Conv2D(32, (3,3), activation="relu", input_shape=(62,47,1)),
    MaxPooling2D((2,2)),
    Conv2D(64, (3,3), activation="relu"),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(128, activation="relu"),
    Dense(len(lfw.target_names), activation="softmax")
])

model.summary()

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2
)

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)

print("\nTest Accuracy:", accuracy)

prediction = model.predict(X_test[0:1], verbose=0)
predicted_index = np.argmax(prediction)

print("Predicted person:", lfw.target_names[predicted_index])
print("Actual person:", lfw.target_names[y_test[0]])

plt.imshow(X_test[0].squeeze(), cmap="gray")
plt.title("Predicted: " + lfw.target_names[predicted_index])
plt.axis("off")
plt.show()