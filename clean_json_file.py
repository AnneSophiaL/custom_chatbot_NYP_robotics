import json
import re

def clean_json_data(input_file, output_file):
    # Ouvrir et lire le fichier JSON d'entrée
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Parcourir chaque cours dans le fichier JSON
    full_time_courses = data.get('fullTimeCourses', [])
    
    for course in full_time_courses:
        # Parcourir chaque année dans le cours
        for year in course.get('years', []):
            # Parcourir chaque module de l'année
            if year != "Year 3":
                for module in year.get('core modules', []):

                    # Nettoyer les espaces inutiles
                    module['title'] = re.sub(r'\s{2,}', '\n', module.get('title', ''))                    
                    module['hours'] = re.sub(r'\s{2,}', '\n', module.get('hours', ''))
                    module['description'] = re.sub(r'\s{2,}', '\n', module.get('description', ''))

            # year = "Year 3" 
            if year.get('elective_programmes'):
                for elective in year.get('elective_programmes', []):
                    for module in elective.get('core modules', []):
                    # Nettoyer les espaces inutiles
                        module['title'] = re.sub(r'\s{2,}', '\n', module.get('title', ''))                        
                        module['hours'] = re.sub(r'\s{2,}', '\n', module.get('hours', ''))
                        module['description'] = re.sub(r'\s{2,}', '\n', module.get('description', ''))

                    for el_module in elective.get('elective modules', []):
                    # Clean unnecessary spaces
                        el_module['title'] = re.sub(r'\s{2,}', '\n', el_module.get('title', '')).strip()                        
                        el_module['hours'] = re.sub(r'\s{2,}', '\n', el_module.get('hours', '')).strip()
                        el_module['description'] = re.sub(r'\s{2,}', '\n', el_module.get('description', '')).strip()

            else:
                for module in year.get('modules', []):
                    for mod in module.get('core modules', []):
                        # Nettoyer les espaces inutiles
                            mod['title'] = re.sub(r'\s{2,}', '\n', mod.get('title', ''))                        
                            mod['hours'] = re.sub(r'\s{2,}', '\n', mod.get('hours', ''))
                            mod['description'] = re.sub(r'\s{2,}', '\n', mod.get('description', ''))

                    for el_module in module.get('elective modules', []):
                    # Clean unnecessary spaces
                        el_module['title'] = re.sub(r'\s{2,}', '\n', el_module.get('title', '')).strip()                        
                        el_module['hours'] = re.sub(r'\s{2,}', '\n', el_module.get('hours', '')).strip()
                        el_module['description'] = re.sub(r'\s{2,}', '\n', el_module.get('description', '')).strip()
    # Enregistrer les données nettoyées dans un nouveau fichier JSON
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=1)

# Appeler la fonction avec les chemins de fichiers appropriés
input_file = 'D:\\ESIEE\\VOYAGE SINGAP 2023\\project_custom_chatbot_nyp\\EWB.json'
output_file = 'D:\\ESIEE\\VOYAGE SINGAP 2023\\project_custom_chatbot_nyp\\EWB_cleaned.json'
clean_json_data(input_file, output_file)
