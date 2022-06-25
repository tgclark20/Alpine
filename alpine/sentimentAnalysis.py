"""
    File name: main.py
    Author: Timothy Clark
    Date created: 06/14/2022
    Date last modified: 06/16/2022
    Python Version: 3.9

    Description: helper methods to train and conduct sentiment analysis on news articles
"""
import AlpacaUtils
import pandas as pd
import nltk
import random 
from nltk.tokenize import RegexpTokenizer
import constants
import pickle
from tqdm import tqdm

tokenizer = RegexpTokenizer(r'\w+')
def trainmodel():
    df = pd.read_csv(constants.TRAIN_DATA,encoding="ISO-8859-1")


    data =[(row[1], row[0]) for index, row in df.iterrows()]



    tokens=set(word.lower() for words in data for word in tokenizer.tokenize(words[0]))
    train = [({word: (word in tokenizer.tokenize(x[0])) for word in tokens}, x[1]) for x in tqdm(data)] 

    random.shuffle(train)

    train_x=train[:3500]
    test_x=train[3501:] 

    model = nltk.NaiveBayesClassifier.train(train_x)
    acc=nltk.classify.accuracy(model, test_x)
    print("Accuracy:", acc)

    model.show_most_informative_features()

    save_classifier = open("naivebayes.pickle","wb")
    pickle.dump(model, save_classifier)
    save_classifier.close()


def classifyArticle(article):
    print("placeholder")

trainmodel()