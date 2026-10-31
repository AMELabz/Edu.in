import os
import string
import pickle
import random
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from PIL import Image
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, add

# STEP 1: DATASET PATHS
image_dir = r"D:/Work/Sairam/Subjects Handled/5. June-Dec 2026/Deep Learning Lab/Exp_11/Data/Flickr8k_Dataset/Flicker8k_Dataset"

text_dir = r"D:/Work/Sairam/Subjects Handled/5. June-Dec 2026/Deep Learning Lab/Exp_11/Data/Flickr8k_text"

caption_file = os.path.join(text_dir, "Flickr8k.token.txt")
if not os.path.exists(caption_file):
    caption_file = os.path.join(text_dir, "Flickr8k.token")

train_file = os.path.join(text_dir, "Flickr_8k.trainImages.txt")
val_file = os.path.join(text_dir, "Flickr_8k.devImages.txt")
test_file = os.path.join(text_dir, "Flickr_8k.testImages.txt")

# STEP 2: DATASET SUMMARY

image_count = sum(
    f.lower().endswith((".jpg", ".jpeg", ".png"))
    for f in os.listdir(image_dir)
)

with open(caption_file, "r", encoding="utf-8") as f:
    caption_count = sum(1 for line in f if line.strip())

def load_split(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

train_names = load_split(train_file)
val_names = load_split(val_file)
test_names = load_split(test_file)

print("========== Flickr8k Dataset Summary ==========")
print("Total images:", image_count)
print("Total captions:", caption_count)
print("Training images:", len(train_names))
print("Validation images:", len(val_names))
print("Testing images:", len(test_names))

# Remove filenames whose image files do not exist
train_names = [
    n for n in train_names
    if os.path.isfile(os.path.join(image_dir, n))
]
val_names = [
    n for n in val_names
    if os.path.isfile(os.path.join(image_dir, n))
]
test_names = [
    n for n in test_names
    if os.path.isfile(os.path.join(image_dir, n))
]

# STEP 3: LOAD AND CLEAN CAPTIONS

def load_captions(filename):
    captions = {}

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")

            if len(parts) != 2:
                continue

            name = parts[0].split("#")[0]
            caption = parts[1].lower()
            caption = caption.translate(
                str.maketrans("", "", string.punctuation)
            )
            caption = "startseq " + caption + " endseq"

            captions.setdefault(name, []).append(caption)

    return captions

captions = load_captions(caption_file)

print("\nCaptions loaded:", len(captions))


# STEP 4: SELECT ALL IMAGES FROM THE SPLITS

all_names = list(dict.fromkeys(train_names + val_names + test_names))

# STEP 5: EXTRACT IMAGE FEATURES USING INCEPTIONV3

base_model = InceptionV3(weights="imagenet")
feature_model = Model(
    inputs=base_model.input,
    outputs=base_model.layers[-2].output
)

features = {}

for i, name in enumerate(all_names):
    image_path = os.path.join(image_dir, name)

    image = Image.open(image_path).convert("RGB")
    image = image.resize((299, 299))
    image = np.array(image, dtype=np.float32)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    feature = feature_model.predict(image, verbose=0)
    features[name] = feature[0]

    if (i + 1) % 500 == 0:
        print("Features extracted:", i + 1, "/", len(all_names))

np.save("D:/Work/Sairam/Subjects Handled/5. June-Dec 2026/Deep Learning Lab/Exp_11/flickr8k_features.npy", features)
print("Image feature extraction completed.")

# STEP 6: PREPARE CAPTIONS AND TOKENIZER

train_captions = []

for name in train_names:
    train_captions.extend(captions[name])

tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_captions)

vocab_size = len(tokenizer.word_index) + 1
max_length = max(len(c.split()) for c in train_captions)

print("Vocabulary size:", vocab_size)
print("Maximum caption length:", max_length)

with open("flickr8k_tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)
    
# STEP 7: CREATE TRAINING SEQUENCES

def create_sequences(image_names):
    X_image = []
    X_sequence = []
    y_word = []

    for name in image_names:
        for caption in captions[name]:
            sequence = tokenizer.texts_to_sequences([caption])[0]

            for i in range(1, len(sequence)):
                input_seq = sequence[:i]
                output_word = sequence[i]

                input_seq = pad_sequences(
                    [input_seq], maxlen=max_length
                )[0]

                X_image.append(features[name])
                X_sequence.append(input_seq)
                y_word.append(output_word)

    return (
        np.array(X_image, dtype=np.float32),
        np.array(X_sequence, dtype=np.int32),
        np.array(y_word, dtype=np.int32)
    )

X1_train, X2_train, y_train = create_sequences(train_names)
X1_val, X2_val, y_val = create_sequences(val_names)

print("Training sequences:", len(y_train))
print("Validation sequences:", len(y_val))

# STEP 8: BUILD THE IMAGE CAPTIONING MODEL

image_input = Input(shape=(2048,))
image_features = Dropout(0.3)(image_input)
image_features = Dense(256, activation="relu")(image_features)

caption_input = Input(shape=(max_length,))
caption_features = Embedding(
    vocab_size, 256, mask_zero=True
)(caption_input)
caption_features = Dropout(0.3)(caption_features)
caption_features = LSTM(256)(caption_features)

decoder = add([image_features, caption_features])
decoder = Dense(256, activation="relu")(decoder)
output = Dense(vocab_size, activation="softmax")(decoder)

model = Model(
    inputs=[image_input, caption_input],
    outputs=output
)

model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer="adam"
)

model.summary()

# STEP 9: TRAIN THE MODEL

history = model.fit(
    [X1_train, X2_train],
    y_train,
    validation_data=([X1_val, X2_val], y_val),
    epochs=5,
    batch_size=256
)

model.save("flickr8k_caption_model.keras")
print("Model training completed and saved.")


# STEP 10: PLOT TRAINING AND VALIDATION LOSS

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Image Captioning Model Loss")
plt.legend()
plt.show()

# STEP 11: GENERATE A CAPTION FOR AN IMAGE

def generate_caption(name):
    image_feature = features[name].reshape(1, 2048)
    caption = "startseq"

    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([caption])[0]
        sequence = pad_sequences(
            [sequence], maxlen=max_length
        )

        prediction = model.predict(
            [image_feature, sequence], verbose=0
        )

        word_index = np.argmax(prediction)
        word = tokenizer.index_word.get(word_index)

        if word is None or word == "endseq":
            break

        caption += " " + word

    return caption.replace("startseq", "").strip()


# STEP 12: DISPLAY A TEST IMAGE AND ITS CAPTION

test_image = test_names[0]
image = Image.open(os.path.join(image_dir, test_image))

plt.imshow(image)
plt.axis("off")
plt.title(generate_caption(test_image))
plt.show()