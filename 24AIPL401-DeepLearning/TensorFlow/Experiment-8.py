import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Embedding, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

file_name = "D:/Work/Sairam/Subjects Handled/5. June-Dec 2026/Deep Learning Lab/Exp_8/data/eng_tamil_pairs.txt"

english = []
tamil = []

with open(file_name, "r", encoding="utf-8") as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        # Separate English and Tamil using TAB
        parts = line.split("\t", 1)

        if len(parts) == 2:

            english_sentence = parts[0].strip()
            tamil_sentence = parts[1].strip()

            english.append(english_sentence)
            tamil.append(tamil_sentence)


print("Number of sentence pairs:", len(english))

unique_pairs = list(dict.fromkeys(zip(english, tamil)))

english = [pair[0] for pair in unique_pairs]
tamil = [pair[1] for pair in unique_pairs]


print("Unique sentence pairs:", len(english))
######################################

tamil = [
    "<start> " + sentence + " <end>"
    for sentence in tamil
]

#create tokenizer
eng_tokenizer = Tokenizer(filters='')
tam_tokenizer = Tokenizer(filters='')
# Learn vocabulary
eng_tokenizer.fit_on_texts(english)
tam_tokenizer.fit_on_texts(tamil)
eng_seq = eng_tokenizer.texts_to_sequences(english)
tam_seq = tam_tokenizer.texts_to_sequences(tamil)

# Finding Maximum length in Eng & Tamil Sentences

max_eng = max(len(x) for x in eng_seq)
max_tam = max(len(x) for x in tam_seq)

print("Maximum English length:", max_eng)
print("Maximum Tamil length:", max_tam)

# Add padding
eng_seq = pad_sequences(eng_seq,maxlen=max_eng,padding="post")
tam_seq = pad_sequences(tam_seq,maxlen=max_tam,padding="post")

eng_vocab = len(eng_tokenizer.word_index) + 1
tam_vocab = len(tam_tokenizer.word_index) + 1

print("Number of sentence pairs:", len(english))
print("Unique sentence pairs:", len(english))
print("Maximum English length:", max_eng)
print("Maximum Tamil length:", max_tam)
print("English vocabulary:", eng_vocab)
print("Tamil vocabulary:", tam_vocab)

# Prepare decoder inputs and outputs
decoder_input = tam_seq[:, :-1]
decoder_output = tam_seq[:, 1:]

# Encoder
encoder_input = Input(shape=(max_eng,),name="encoder_input")
encoder_embedding = Embedding(eng_vocab,64)(encoder_input)
encoder_lstm = LSTM(128,return_state=True)
_, h, c = encoder_lstm(encoder_embedding)

#Decoder
decoder_input_layer = Input(shape=(max_tam - 1,), name="decoder_input")
decoder_embedding = Embedding(tam_vocab,64)(decoder_input_layer)
decoder_lstm = LSTM(128,return_sequences=True)
decoder_output_layer = decoder_lstm(decoder_embedding,initial_state=[h, c])
output = Dense(tam_vocab,activation="softmax")(decoder_output_layer)

#Create Encoder-Decoder model
model = Model([encoder_input, decoder_input_layer], output)
#Compile model
model.compile(optimizer="adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"])
model.summary()

model.fit(
    [eng_seq, decoder_input],
    np.expand_dims(decoder_output, -1),
    epochs=100,
    batch_size=32,
    verbose=1
)

reverse_tamil = {
    value: key
    for key, value in tam_tokenizer.word_index.items()
}

def translate(sentence):

    # Convert English sentence into numbers
    sequence = eng_tokenizer.texts_to_sequences(
        [sentence]
    )

    # Apply padding
    sequence = pad_sequences(
        sequence,
        maxlen=max_eng,
        padding="post"
    )


    # Get START and END token numbers
    start = tam_tokenizer.word_index["<start>"]
    end = tam_tokenizer.word_index["<end>"]


    # Start Tamil sentence
    target = [start]


    # Generate Tamil words one by one
    for i in range(max_tam - 1):

        target_seq = pad_sequences(
            [target],
            maxlen=max_tam - 1,
            padding="post"
        )


        # Predict next word
        prediction = model.predict(
            [sequence, target_seq],
            verbose=0
        )


        # Select word with highest probability
        next_word = np.argmax(
            prediction[0, len(target) - 1, :]
        )


        # Stop when END token is generated
        if next_word == end or next_word == 0:
            break


        target.append(next_word)


    # Convert numbers back to Tamil words
    result = []

    for word_id in target[1:]:

        if word_id in reverse_tamil:

            word = reverse_tamil[word_id]

            if word != "<start>" and word != "<end>":
                result.append(word)


    return " ".join(result)



# Few Examples



test_sentences = [
    "Get down.",
    "Goodbye and take care.",
    "Let's meet again soon.",
    "Good morning.",
    "Thank you.",
    "How are you?"
]


for sentence in test_sentences:

    print("\nEnglish :", sentence)
    print("Tamil   :", translate(sentence))
    
test_sentences = ["hospital"]


for sentence in test_sentences:

    print("\nEnglish :", sentence)
    print("Tamil   :", translate(sentence))



