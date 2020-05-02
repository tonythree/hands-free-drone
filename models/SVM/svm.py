from sklearn.svm import SVC
import csv
from pathlib import Path
import numpy as np
from sklearn.model_selection  import GridSearchCV
#from sklearn.learning_curve import validation_curve


data_folder = Path("/data/csv/")



folders = data_folder / "experiments.csv"

f = open(folders)
csv_f = csv.reader(f)

list1=[] 

for row in csv_f:
    list1.append(row)

table = np.asarray(list1, dtype=np.float64)
print(table.shape)

x_train=table[0:192, 1:5]   #60% data = training  
y_train=table [0:192,11:12]



print(x_train.shape, y_train.shape)

Cs = np.logspace(-6, 3, 10)
parameters = [{'kernel': ['rbf'], 'C': Cs},
              {'kernel': ['linear'], 'C': Cs}]

svc = SVC(random_state = 12)

clf = GridSearchCV(estimator = svc, param_grid = parameters, cv = 4, n_jobs = -1)#cv=5
clf.fit(x_train, y_train.flatten())

print(clf.best_params_)
print(clf.best_score_)


x_test=table[192:320, 1:5]    #40% data =testing
y_test=table [192:320,11:12]

print("testing results")
print(clf.score(x_test, y_test))