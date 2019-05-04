#########Import Dependencies#############################################################
import pandas as pd
from collections import defaultdict

#########importing dataset#############################################################
df = pd.read_excel("raw_data.xlsx")    #excel file is imported


######data cleaning##################################################################################
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
 

######getting count of each symptom###################################################           
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
            
            
####taking input#################################################################           
i = []  

i_dict = []
for s in i:
    i_dict.append([s, freq_symptom[s]])
    
final = sorted(i_dict, key=lambda x: x[1])    
    
disease = disease_symptom_dict.keys()    
for value in final:
    lst1 = sym_disease[value[0]]
    lst = [val for val in lst1 if val in disease]
    if len(lst) >= 1: 
        disease = lst
    else:
        break


#importing dataset for test required#############################################
df_new = pd.read_csv("data.csv", header = None)

test = {}

f_col = df_new.iloc[: , 0:1].values

l = df_new.iloc[: , 1: ].values

for i in range(len(f_col)):
    temp = []
    for j in range(4):
        if l[i][j] != 'na':
            temp.append(l[i][j])
    test[f_col[i][0]] = temp    

output = []
for dis in disease:
    try:
        list1 = test[dis]
    except KeyError as e:
        pass
    for x in list1:
        output.append(x.lower().lstrip())
        
from collections import Counter

def top_k(list, k=2):
    c = Counter(list)
    most_common = [key for key, val in c.most_common(k)]
    return most_common   
#output for display#################################################
output = top_k(output)
 
                    