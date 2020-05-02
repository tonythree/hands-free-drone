import csv
from pathlib import Path
import numpy as np



data_folder = Path("/data/csv/")


# Open csv files 

folders = data_folder / "files"



f1 = open(folders)
csv_f1 = csv.re ader(f1)
l=0

#Initialize the table of features
feature = np.zeros((145,37),dtype=np.float64)

#print(feature.shape)

for line in csv_f1:
  s=""
  s=s.join(line)
  print(s)

  file_to_open = data_folder/ s
  print(file_to_open)

  f = open(file_to_open)
  csv_f = csv.reader(f) 

  list1=[] 

  for row in csv_f:
    list1.append(row)

  #Table of the raw cleaned features
  table = np.asarray(list1, dtype=np.float64)
  k=0 #initialisation de k 0
  

  

  for i in range(1,5):
    if ((i!= 4) and (i!= 5) and (i!= 6)):

      #print("************************")
      #print(i)
      #print(k)
      feature[l,k]=table[:,i].mean()
      feature[l,k+1]=table[:,i].std()
      feature[l,k+2]=np.min(table[:,i])
      feature[l,k+3]=np.max(table[:,i])
      #print(l)
      
      
      k=k+4

  l=l+1
 

labels = data_folder / "labels.csv"
f = open(labels)
csv_f = csv.reader(f)

list1=[] 

for row in csv_f:
    list1.append(row)

table = np.asarray(list1, dtype=np.int)
'''
print(labels)
print(table.shape)
print(table.shape[1])
'''


index=0

for i in range(table.shape[1]):
  #print("debut")
  #print(index)
  j=0

  feature[index:index+table[j,i],8]=0    #average of movement 
  index=index+table[j,i]
   
   

  feature[index:index+table[j+1,i],36]=1
  index=index+table[j+1,i]
    
  '''
  feature[index:index+table[j+2,i],36]=3
  index=index+table[j+2,i]


  feature[index:index+table[j+3,i],36]=4

  print(index, index+table[j+3,i])
  #print("feature[index,36]")
  print(feature[index,36])

  index=index+table[j+3,i]
   
  #print("la fin")
  print(table[j+3,i])
  print(index)
  '''

  


    
  


#print(feature)
np.savetxt(data_folder/"experiments.csv", feature, delimiter=",")    

