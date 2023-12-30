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
training_set = pd.read_csv('Data/Training.csv')
testing_set = pd.read_csv('Data/Testing.csv')

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

#Calcoliamo le varie importanze delle feature nel modello Decision Tree
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = columns

#Instanziamo i dizionari
severityDictionary = dict()
desrciptionDictionary = dict()
precautionDictionary = dict()

symtompsDict = {}

#Associamo ai nomi dei sintomi gli indici corrispondenti
for index, symptom in enumerate(x_train):
    symtompsDict[symptom] = index

#Otteniamo le descrizioni dei sintomi dal file symptom_Description.csv e popoliamo la variabile globale desrciptionList
def getDescription():
    global desrciptionList
    with open('MasterData/symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter= ',')
        try:
            for row in csv_reader:
                _description = {row[0]: row[1]}
                desrciptionList.update(_description)
        except Exception as e:
            logging.error("Si è verificato un errore imprevisto.")


#def getSeverity():

"""
Ottengo le informazioni riguardo le precauzioni da prendere per le malattie trovate dal file symptom_precaution.csv e popolo
la variabile globale (!!!è un dizionario!!!) precautionDictionary
"""
def getprecautionDict():
    global precautionDictionary
    with open('MasterData/symptom_precaution.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        try:
            for row in csv_reader:
                #Uso la funzione _prec per popolare la var. globale; estraggo il nome del sintomo (row[0]) e le 4 prec. consigliate (row[1],row[2],row[3],row[4])
                _prec = {row[0]: [row[1], row[2], row[3], row[4]]}
                precautionDictionary.update(_prec)
        except Exception as e:
            logging.error("Si è verificato un errore imprevisto.")

#Ottengo le informazioni del pazione

def getInfo():
    print("\nCiao!\nSono MediAI, un bot intelligente che aiuta per capire cosa potresti avere.\nCome ti chiami?\t")
    name = input("")
    print("Ciao, "+ name +".")