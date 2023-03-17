import random
import json
import pickle
import numpy as np
import nltk

from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
name = "Alexa"
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_words(sentence):
    sentence_words = clean_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict(sentence):
    bow = bag_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR = 0.25
    result = [[i,r] for i, r in enumerate(res) if r > ERROR]

    result.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in result:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_intents = intents_json['intents']
    for i in list_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("Bot is running")

while True:
    try:
        message = input("")
        ints = predict(message)
        res = response(ints, intents)
        print(res)
        print("\nNext Question: ")
    except:
        print("I'm still learning!! Tell me something else")