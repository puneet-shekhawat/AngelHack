# Import Dependencies
import csv
import pandas as pd
import numpy as np
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt

#importing dataset
df = pd.read_excel("raw_data.xlsx")



data = df.fillna(method='ffill')


# Process Disease and Symptom Names
def process_data(data):
    data_list = []
    data_name = data.replace('^','_').split('_')
    n = 1
    for names in data_name:
        if (n % 2 == 0):
            data_list.append(names)
        n += 1
    return data_list

disease_list = []
disease_symptom_dict = defaultdict(list)
disease_symptom_count = {}
count = 0

for idx, row in data.iterrows():
    
    # Get the Disease Names
    if (row['Disease'] !="\xc2\xa0") and (row['Disease'] != ""):
        disease = row['Disease']
        disease_list = process_data(data=disease)
        count = row['Count of Disease Occurrence']

    # Get the Symptoms Corresponding to Diseases
    if (row['Symptom'] !="\xc2\xa0") and (row['Symptom'] != ""):
        symptom = row['Symptom']
        symptom_list = process_data(data=symptom)
        for d in disease_list:
            for s in symptom_list:
                disease_symptom_dict[d].append(s)
            disease_symptom_count[d] = count
 

#getting count of each symptom           
symptoms = list(disease_symptom_dict.values())  
freq_symptom = {} 
sym_disease = {}     

            
for row in disease_symptom_dict:
         for y in disease_symptom_dict[row]:
             if y != "":
                 freq_symptom[y] = freq_symptom.get(y, 0) + 1
                 if y in sym_disease.keys():
                     sym_disease[y].append(row)
                 else:
                     sym_disease[y] = []
                     sym_disease[y].append(row)
            
            
            
i = ["cough", "chill", "fever"]  

i_dict = []
for s in i:
    i_dict.append([s, freq_symptom[s]])
    
final = sorted(i_dict, key=lambda x: x[1])    
    
disease = disease_symptom_dict.keys()    
for value in final:
    #print(value[0])
    
    lst1 = sym_disease[value[0]]
    #print(lst1)
    lst = [val for val in lst1 if val in disease]
    if len(lst) >= 1: 
        disease = lst
    else:
        break
                