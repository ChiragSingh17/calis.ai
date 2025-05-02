import pandas as pd
import numpy as np


data=pd.read_csv("spam.csv", encoding="latin-1")

data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)

data['class']=data['class'].map({'ham':0, 'spam':1})

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.model_selection import train_test_split
X=data['message']
y=data['class']

cv=CountVectorizer()

X=cv.fit_transform(X)

x_train, x_test,y_train, y_test=train_test_split(X,y, test_size=0.2, random_state=42)

from sklearn.naive_bayes import MultinomialNB

model=MultinomialNB()

model.fit(x_train, y_train)

model.score(x_test, y_test)

msg = input("Enter Text : ")
data = [msg]
vect = cv.transform(data).toarray()
my_prediction = model.predict(vect)

import pickle
pickle.dump(model, open('spam.pkl','wb'))
model1 = pickle.load(open('spam.pkl','rb'))

def result(msg):
    data = [msg]
    vect = cv.transform(data).toarray()
    my_prediction = model1.predict(vect)
    if my_prediction[0]==1:
        print("This is a Spam mail")
    else:
        print("This is NOT a Spam mail")

result(msg)