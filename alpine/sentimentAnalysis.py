import AlpacaUtils
import pandas as pd
import nltk
import random 
from nltk.tokenize import word_tokenize
import constants

df = pd.read_csv(constants.TRAIN_DATA,encoding="ISO-8859-1")


data =[(row[1], row[0]) for index, row in df.iterrows()]

print(data[0:5])

tokens=set(word.lower() for words in data for word in word_tokenize(words[0]))
train = [({word: (word in word_tokenize(x[0])) for word in tokens}, x[1]) for x in data] 

random.shuffle(train)

train_x=train[:3000]
test_x=train[3001:] 

model = nltk.NaiveBayesClassifier.train(train_x)
acc=nltk.classify.accuracy(model, test_x)
print("Accuracy:", acc)

model.show_most_informative_features()