import random
import json
import numpy as np
import pickle

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.python import keras

from keras.models import load_model

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def askBot():
    user_input = request.args.get("input")
    results = predict_class(user_input)
    tag = results[0]['intent']
    intent = next(item for item in intents["intents"] if item["tag"] == tag)
    response = "Bot: " + random.choice(intent["responses"])
    return jsonify(message=response)
    # print("Bot: " + random.choice(intent["responses"]))


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

model = load_model('chatbot_model.h5')


def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1

    return np.array(bag)


def predict_class(sentence):
    # filter out predictions below a threshold
    bow = bag_of_words(sentence)

    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def main():
    while True:
        user_input = input("You: ")
        if user_input == "quit":
            break
        results = predict_class(user_input)
        tag = results[0]['intent']
        intent = next(item for item in intents["intents"] if item["tag"] == tag)
        print("Bot: " + random.choice(intent["responses"]))


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
