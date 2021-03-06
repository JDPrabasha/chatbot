

import random
import json
import numpy as np
import pickle

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.python import keras

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import gradient_descent_v2


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignore_words = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        # add documents in the corpus
        documents.append((word_list, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower())
         for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    pattern_words = document[0]
    pattern_words = [lemmatizer.lemmatize(
        word.lower()) for word in pattern_words]
    for word in words:
        if word in pattern_words:
            bag.append(1)
        else:
            bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = gradient_descent_v2.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])

model.fit(np.array(train_x), np.array(train_y),
          epochs=200, batch_size=5, verbose=1)

model.save('chatbot_model.h5')
print("Model Saved")
