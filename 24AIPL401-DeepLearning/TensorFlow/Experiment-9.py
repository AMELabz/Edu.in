import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers

# Load data
(x_train_raw, y_train), (x_test_raw, y_test) = tf.keras.datasets.fashion_mnist.load_data()
x_train_raw = x_train_raw[..., None]
x_test_raw = x_test_raw[..., None]

# GAN data [-1, 1]
x_train_gan = (x_train_raw.astype("float32") - 127.5) / 127.5

# Classifier data [0, 1]
x_train_cls = x_train_raw.astype("float32") / 255.0
x_test_cls = x_test_raw.astype("float32") / 255.0

print("GAN training data:", x_train_gan.shape)
print("Classifier training data:", x_train_cls.shape)
print("Test data:", x_test_cls.shape)


# ---------------- Generator ----------------
G = tf.keras.Sequential([
    layers.Input(shape=(100,)),
    layers.Dense(7*7*256, use_bias=False),
    layers.BatchNormalization(),
    layers.LeakyReLU(),
    layers.Reshape((7,7,256)),
    layers.Conv2DTranspose(128, 4, 2, padding="same", use_bias=False),
    layers.BatchNormalization(),
    layers.LeakyReLU(),
    layers.Conv2DTranspose(64, 4, 2, padding="same", use_bias=False),
    layers.BatchNormalization(),
    layers.LeakyReLU(),
    layers.Conv2D(1, 3, padding="same", activation="tanh")
])

# ---------------- Discriminator ----------------
D = tf.keras.Sequential([
    layers.InputLayer(input_shape=(28,28,1)),
    layers.Conv2D(64, 4, 2, padding="same"),
    layers.LeakyReLU(0.2),
    layers.Dropout(0.3),
    layers.Conv2D(128, 4, 2, padding="same"),
    layers.LeakyReLU(0.2),
    layers.Dropout(0.3),
    layers.Flatten(),
    layers.Dense(1, activation="sigmoid")
])

D.compile(optimizer=tf.keras.optimizers.Adam(0.0002, 0.5), loss="binary_crossentropy")

# GAN
D.trainable = False
GAN = tf.keras.Sequential([G, D])
GAN.compile(optimizer=tf.keras.optimizers.Adam(0.0002, 0.5), loss="binary_crossentropy")

# Train GAN
epochs = 50
batch_size = 128

for epoch in range(epochs):
    for i in range(0, len(x_train_gan), batch_size):
        real = x_train_gan[i:i+batch_size]
        n = len(real)

        noise = np.random.normal(0, 1, (n, 100))
        fake = G.predict(noise, verbose=0)

        D.trainable = True
        D.train_on_batch(real, np.ones((n,1))*0.9)
        D.train_on_batch(fake, np.zeros((n,1)))

        D.trainable = False
        noise = np.random.normal(0, 1, (n,100))
        GAN.train_on_batch(noise, np.ones((n,1)))

    print("Epoch:", epoch+1)

# Generate images
noise = np.random.normal(0, 1, (16,100))
generated = G.predict(noise, verbose=0)
generated = (generated + 1) / 2

# Display generated images
plt.figure(figsize=(8,8))
for i in range(16):
    plt.subplot(4,4,i+1)
    plt.imshow(generated[i].squeeze(), cmap="gray")
    plt.axis("off")
plt.suptitle("GAN Generated Images")
plt.tight_layout()
plt.show()

# Generate synthetic data
num_fake = 5000
noise = np.random.normal(0, 1, (num_fake,100))
fake_images = G.predict(noise, verbose=0)
fake_images = (fake_images + 1) / 2

print("Generated images:", fake_images.shape)

# Classifier
def create_classifier():
    model = tf.keras.Sequential([
        layers.Input(shape=(28,28,1)),
        layers.Conv2D(32,3,activation="relu"),
        layers.MaxPooling2D(),
        layers.Conv2D(64,3,activation="relu"),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(64,activation="relu"),
        layers.Dense(10,activation="softmax")
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model

# Original classifier
print("Training original classifier...")
model_original = create_classifier()
model_original.fit(x_train_cls, y_train, epochs=3, batch_size=128, verbose=1)
_, accuracy_original = model_original.evaluate(x_test_cls, y_test, verbose=0)

# Augmented dataset
fake_labels = np.random.choice(y_train, num_fake)
x_augmented = np.concatenate([x_train_cls, fake_images])
y_augmented = np.concatenate([y_train, fake_labels])

idx = np.random.permutation(len(x_augmented))
x_augmented = x_augmented[idx]
y_augmented = y_augmented[idx]

print("Augmented data:", x_augmented.shape)

# Augmented classifier
print("Training augmented classifier...")
model_augmented = create_classifier()
model_augmented.fit(x_augmented, y_augmented, epochs=3, batch_size=128, verbose=1)
_, accuracy_augmented = model_augmented.evaluate(x_test_cls, y_test, verbose=0)

# Results
print("\nOriginal Accuracy:", accuracy_original*100, "%")
print("GAN Augmented Accuracy:", accuracy_augmented*100, "%")
print("Change:", (accuracy_augmented-accuracy_original)*100, "%")

# Accuracy graph
plt.figure(figsize=(7,5))
plt.bar(["Original", "GAN Augmented"], [accuracy_original*100, accuracy_augmented*100])
plt.ylabel("Accuracy (%)")
plt.title("Classification Accuracy")
plt.ylim(0,100)
plt.show()
