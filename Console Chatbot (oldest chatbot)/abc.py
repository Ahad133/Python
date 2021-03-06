#imported code
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import nltk

#nltk.download('punkt')

#"D:\Coding\Python\Chatbot\Chat.json"
#r"C:\\Users\\ayaz\\Desktop\\New folder\\New folder\\Python\\Chatbot\\Chat.json"
  
with open(r"C:\\Users\\ayaz\\Desktop\\New folder\\New folder\\Python\\Chatbot\\Chat.json") as file:
    data = json.load(file)

# in this code its not training its direclty starting withouth even making a pickle nvm it did just in another dir for me 
# i am going to comment this one out aswewll

# another thing i learned our data is directly off the chats its not professional by any means 

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []


    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

#tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# going to comment this code out to see if hes going to train him in a loop
# try:
#     model.load("model.tflearn")

# except:
#     model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
#     model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])[0]  # gives probability of the output in percentage
        results_index = numpy.argmax(results)  # gives us the index of the greatest probability to display
        tag = labels[results_index]  # get the tags which have the highest probability

        # if bot gets some random question it wouldn't go gibberish instead response smart
        if results[results_index] > 0.70:  # if the probability is above 70% it will show the response
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']  # choose the response

            print(random.choice(responses))  # randomize the response
        else:  # if probability is less than 70% it will run this block
            print("I didn't understand.")


chat()


# old cod which does not include probability
# def chat():
#     print("Start talking with the bot (type quit to stop)!")
#     while True:
#         inp = input("You: ")
#         if inp.lower() == "quit":
#             break

#         results = model.predict([bag_of_words(inp, words)])
#         results_index = numpy.argmax(results)
#         tag = labels[results_index]

#         for tg in data["intents"]:
#             if tg['tag'] == tag:
#                 responses = tg['responses']

#         print(random.choice(responses))


# chat()