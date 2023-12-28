import csv
import re
import warnings
import numpy as np
import pandas as pd
import logging
from googletrans import Translator
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.metrics import precision_score, classification_report

translator = Translator()

#Carico i dataset di training e testing
training_set = pd.read_csv('Datasets/Training.csv')
testing_set = pd.read_csv('Datasets/Testing.csv')

#prendo le colonne del training set
columns = training_set.columns
#tolgo l'ultima colonna, la quale rappresenta la varaibile dipendente
columns = columns[:-1]

#estraggo features e creo la variabile dipendente
x_train = training_set[columns]
y_train = training_set['prognosis']

#Poiché necessitiamo di valori numerici, mappiamo le stringhe in numeri con un encoder
le = preprocessing.LabelEncoder()
le.fit(y_train)
y_train = le.transform(y_train)

#poiché ho i due set di training e testing, non vado a dividere, ma sfrutto i due dataset
x_test = testing_set[columns]
y_test = testing_set['prognosis']
y_test = le.transform(y_test)

#Creiamo ora il classificatore: per la natura del problema utilizziamo un classificatore DecisionTree

classifier = DecisionTreeClassifier()
classifier = classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

print(classification_report(y_test, y_pred))

print(classifier.score(x_test, y_test))


