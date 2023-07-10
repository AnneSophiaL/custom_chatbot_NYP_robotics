import json

# Lire le premier fichier JSON
with open('D:\\ESIEE\\VOYAGE SINGAP 2023\\project_custom_chatbot_nyp\\EWB_cleaned.json', 'r') as file1:
    data1 = json.load(file1)

# Lire le second fichier JSON
with open('D:\\ESIEE\\VOYAGE SINGAP 2023\\project_custom_chatbot_nyp\\R&M_cleaned.json', 'r') as file2:
    data2 = json.load(file2)

# Concaténer les données (assumant que data1 et data2 sont des dictionnaires, ajuster selon la structure réelle)
data1['fullTimeCourses'].extend(data2['fullTimeCourses'])

# Écrire les données combinées dans un nouveau fichier
with open('D:\ESIEE\VOYAGE SINGAP 2023\project_custom_chatbot_nyp\combined.json', 'w') as outfile:
    json.dump(data1, outfile)
