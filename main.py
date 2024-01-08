import csv
import re
import warnings
import numpy as np
import pandas as pd
import logging
from googletrans import Translator
from sklearn import preprocessing
from sklearn.model_selection import cross_validate
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.metrics import classification_report

translator = Translator()

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Carico i dataset di training e testing
training_set1 = pd.read_csv('Data/Training.csv')
training_set = training_set1.drop_duplicates()

# prendo le colonne del training set
columns = training_set.columns
# tolgo l'ultima colonna, la quale rappresenta la varaibile dipendente
columns = columns[:-1]

# estraggo features e creo la variabile dipendente
x = training_set[columns]
y = training_set['prognosis']

# Poiché necessitiamo di valori numerici, mappiamo le stringhe in numeri con un encoder
le = preprocessing.LabelEncoder()
le.fit(y)  # funziona anche senza encoding, valutare se inserirlo
y = le.transform(y)

# poiché ho i due set di training e testing, non vado a dividere, ma sfrutto i due dataset
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

# Creiamo ora il classificatore: per la natura del problema utilizziamo un classificatore DecisionTree
classifier = DecisionTreeClassifier()
classifier = classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

print(classification_report(y_test, y_pred))

print(classifier.score(x_test, y_test))

reduced_data = training_set.groupby(training_set['prognosis']).max()

# convalida incrociata
# scores = cross_val_score(classifier, x_test, y_test, cv=5) # se usiamo training e testing set forniti (separati) non possiamo effettuare la cross validation
score = cross_validate(classifier, x_test, y_test, cv=5)
# print("Cross Validation: " + str(scores.mean()))
print("Prestazioni Decision Tree")
print("Fit time: " + str(score['fit_time'].mean()) + "\nScore Time: " + str(
    score['score_time'].mean()) + "\nTest score: " + str(score['test_score'].mean()) + "\n")

# modello Support Vector Machine
model_svc = SVC()
model_svc.fit(x_train, y_train)
print("\nPrestazioni SCV: " + str(model_svc.score(x_test, y_test)))
# prestazioni dell'SVC
score_SVC = cross_validate(model_svc, x_test, y_test, cv=5)
print(score_SVC['fit_time'].mean())
print("Fit time: " + str(score_SVC['fit_time'].mean()) + "\nScore Time: " + str(
    score_SVC['score_time'].mean()) + "\nTest score: " + str(score_SVC['test_score'].mean()) + "\n")

y_pred_svc = model_svc.predict(x_test)
print(classification_report(y_test, y_pred_svc))

# modello naive bayes
naive = BernoulliNB()
naive.fit(x_train, y_train)
probab = naive.predict_proba(x_test)
nbscore = naive.score(x_test, y_test)
print("\nNaive Bayes Probabilities: " + str(nbscore))
score_nb = cross_validate(model_svc, x_test, y_test, cv=5)
print(score_nb['fit_time'].mean())
print("Fit time: " + str(score_nb['fit_time'].mean()) + "\nScore Time: " + str(
    score_nb['score_time'].mean()) + "\nTest score: " + str(score_nb['test_score'].mean()) + "\n")

y_pred_nb = naive.predict(x_test)
print(classification_report(y_test, y_pred_nb))

# Calcoliamo le varie importanze delle feature nel modello Decision Tree
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = columns

# Instanziamo i dizionari
severityDictionary = dict()
descriptionDictionary = dict()
precautionDictionary = dict()

symtompsDict = {}

# Associamo ai nomi dei sintomi gli indici corrispondenti
for index, symptom in enumerate(x_train):
    symtompsDict[symptom] = index


# Otteniamo le descrizioni dei sintomi dal file symptom_Description.csv e popoliamo la variabile globale desrciptionList
def getDescription():
    global descriptionDictionary
    with open('MasterData/symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        try:
            for row in csv_reader:
                _description = {row[0]: row[1]}
                descriptionDictionary.update(_description)
        except Exception as e:
            logging.error("Si è verificato un errore imprevisto.")


# def getSeverity():

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
                # Uso la funzione _prec per popolare la var. globale; estraggo il nome del sintomo (row[0]) e le 4 prec. consigliate (row[1],row[2],row[3],row[4])
                _prec = {row[0]: [row[1], row[2], row[3], row[4]]}
                precautionDictionary.update(_prec)
        except Exception as e:
            logging.error("Si è verificato un errore imprevisto.")


# Ottengo le informazioni del pazione
def getInfo():
    print("\nCiao!\nSono MediAI, un bot intelligente che aiuta per capire cosa potresti avere.\nCome ti chiami?\t")
    name = input("")
    print("Ciao, " + name + ".")

# Cerco un sintomo specifico all'interno di una lista di nomi di sintomi
def check_pattern(dis_list, inp):
    pred_list = []
    inp = inp.replace(' ', '_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list = [item for item in dis_list if regexp.search(item)]
    if len(pred_list) > 0:
        return 1, pred_list
    else:
        return 0, []


# Effetuo una seconda previsione basata sui sintomi specifici forniti come input
def sec_predict(symptoms_exp):
    #training_set = pd.read_csv('Data/Training.csv')
    X = training_set.iloc[:, :-1]
    y = training_set['prognosis']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symtompsDict = {symptom: index for index, symptom in enumerate(X.columns)}

    input_vector = np.zeros(len(symtompsDict))

    for item in symptoms_exp:
        if item in symtompsDict:
            input_vector[[symtompsDict[item]]] = 1
        else:
            print("Sintomo non trovato nel dataset")

    return rf_clf.predict([input_vector])


def calc_condition(exp, days):
    severity_sum = 0
    for item in exp:
        if item in severityDictionary:
            severity_sum += severityDictionary[item]
    if (severity_sum * days) / (len(exp) + 1) > 8:
        print("Ti consiglio di andare da un medico e prendere delle precauzioni.")
    else:
        print("Ti consiglio di sederti e rilassarti: non è necessaria una visita medica.")


def getSeverityDict():
    global severityDictionary
    with open('MasterData/Symptom_severity.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        try:
            for row in csv_reader:
                if len(row) >= 2:
                    _diction = {row[0]: int(row[1])}
                    severityDictionary.update(_diction)
                else:
                    logging.warning(f"Ignorato: {row} - La riga non contiene abbastanza elementi.")
        except Exception as e:
            logging.error(f"Si è verificato un errore imprevisto: {str(e)}")


def print_disease(node):
    node = node[0]
    val = node.nonzero()
    disease = le.inverse_transform(val[0])
    return list(map(lambda x: x.strip(), list(disease)))


# Funzione core del progetto
def tree_to_code(tree, feature_names):
    global num
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined"
        for i in tree_.feature
    ]

    chk_dis = ",".join(feature_names).split(",")
    symtomps_present = []

    while True:
        print("Che sintomo stai riscontrando?\t")
        disease_input = input("")
        disease_input.replace(" ", "_")
        conf, cnf_dis = check_pattern(chk_dis, translator.translate(disease_input, src="it").text)
        if conf == 1:
            print("Ho trovato i seguenti sintomi in base alla tua risposta: ")
            for num, it in enumerate(cnf_dis):
                print(num, ")", translator.translate(it.replace("_", " "), dest="it").text)
            if num != 0:
                print(f"Che sintomo in particolare? (0 -{num}): ", end="")
                conf_inp = int(input(""))
            else:
                conf_inp = 0
            disease_input = cnf_dis[conf_inp]
            break
        else:
            print("Inserisci un sintomo valido.")

    while True:
        try:
            num_days = int(input("Da quanti giorni? "))
            break
        except:
            print("Inserisci un input valido.")

    def diagnose(node, depth):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name, threshold = feature_name[node], tree_.threshold[node]
            val = 1 if name == disease_input else 0

            next_node = tree_.children_left[node] if val <= threshold else tree_.children_right[node]
            diagnose(next_node, depth + 1)
        else:
            present_disease = print_disease(tree_.value[node])
            symtomps_given = reduced_data.columns[reduced_data.loc[present_disease].values[0].nonzero()]
            print("Stai sperimentando qualche sintomo tra questi?")
            symptoms_exp = []
            for sym in list(symtomps_given):
                if sym != disease_input:
                    print(translator.translate(sym.replace("_", " "), dest="it").text + "?", end=" ")
                    while True:
                        inp = input("")
                        if inp == "si" or inp == "no":
                            break
                        else:
                            print("Dai una risposta valida, i.e. (si/no): ", end="")
                        if inp == "si":
                            sym.replace(" ", "_")
                            symptoms_exp.append(sym)

            #second_prediction = sec_predict(symptoms_exp)

            disease = translator.translate(present_disease[0], dest="it").text
            diagnosis_text = f"\nIn base alle mie ricerche potresti avere {disease}"
            """
            if present_disease[0] != second_prediction[0]:
                second_prediction[0] = translator.translate(second_prediction[0], dest="it").text
                diagnosis_text += f" o {second_prediction[0]}"
            """
            print(translator.translate(diagnosis_text, dest="it").text)

            print("\n" + translator.translate(descriptionDictionary[present_disease[0]], dest="it").text)
            print("Prendi le seguenti precauzioni:")
            for i, precaution in enumerate(precautionDictionary[present_disease[0]], 1):
                precaution = translator.translate(precaution, dest="it").text
                print(f"{i}) {precaution}")
        """
            if present_disease[0] != second_prediction[0]:
                prediction = translator.translate(second_prediction[0], src="it").text
                print("\n" + translator.translate(descriptionDictionary[prediction], dest="it").text)

            print("Prendi le seguenti precauzioni:")
            for i, precaution in enumerate(
                    precautionDictionary[translator.translate(second_prediction[0], src="it").text], 1):
                precaution = translator.translate(precaution, dest="it").text
                print(f"{i}) {precaution}")
        """
    diagnose(0, 1)


if __name__ == '__main__':
    getSeverityDict()
    getDescription()
    getprecautionDict()
    getInfo()
    tree_to_code(classifier, columns)
