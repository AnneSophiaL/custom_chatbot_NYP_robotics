from selenium import webdriver 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import jsonlines

# code that comes from :"https://www.geeksforgeeks.org/convert-html-source-code-to-json-object-using-python/"
# Sample URL to fetch the html page
url = "https://www.nyp.edu.sg/schools/seg/full-time-courses/robotics-and-mechatronics.html"

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")
PATH = 'D:\ESIEE\VOYAGE SINGAP 2023\project\Chromedriver'
service = Service(PATH)  # Replace "path_to_chromedriver" with the actual path to chromedriver

# Create a new Selenium driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Get the page through get() method
driver.get(url)

# Save the page content as NYP_robotics.html
# with open("NYP_robotics2.html", "w", encoding='utf8') as html_file:
# 	html_file.write(driver.page_source) 
	
# # ----------------------------------------------------
with open("NYP_robotics2.html", "r", encoding='utf8') as html_file:
    html = html_file.read()
####----------------------------------------------------####

soup = BeautifulSoup(html, 'html.parser')

# Programmes of Year 3
# accordion_panel = soup.find_all(class_="accordionPanel")[2]
# # core_modules_section = accordion_panel.find(class_="richtext parbase section")
# core_modules_section = accordion_panel.find(class_="panel-body")
# # core_modules_section = accordion_panel.find(class_="ds-popbox-container ds-popbox-is-onload")

# module_links = core_modules_section.find_all(['h4','p'])
# module_names_3 = [link.text.strip() for link in module_links]
# print(module_names[1]) # Automation & Robotics Technology
# for name in module_names_3:
  # module_names_pd_y3['Year 3'] = pd.DataFrame(module_names_3)
# for name in module_names_3:
#         print(name) #only got "Elective Programmes,(Choose one specialisation) "
# ------------------------------------------------------------------- #

full_time_course_name = soup.find('title').text.strip() # Diploma in Robotics & Mechatronics
# print(full_time_course_name.text.strip())

years = soup.find_all(text=lambda text: text and 'Year' in text) # ['Year 1', 'Year 2', 'Year 3']
# print(years)
# years = years[:-2]

# -------------------------------------------------------------------

# code working begins here !
# this is for year 1 & 2 (& 3)
# def creation_df_years(soup, years):
#   module_names_pd = pd.DataFrame()
#   module_names_pd_y3 = pd.DataFrame()
#   max = len(years) # = 3
#   for i in range (0,max-1): # (0, 1)
#       accordion_panel = soup.find_all(class_="accordionPanel")[i]

#       # Find the core modules section within the second accordion panel
#       core_modules_section = accordion_panel.find(class_="ds-popbox-content")

#       # Find all the <h4> and <p> tags within the core modules section
#       module_links = core_modules_section.find_all(['h4','p'])

#       # Extract the module names
#       module_names = [link.text.strip() for link in module_links]
#       module_names_pd['Year ',i+1] = pd.DataFrame(module_names)
#       module_names_pd = module_names_pd.rename(columns={module_names_pd.columns[i]: f"Year {i+1}"})

#   accordion_panel_3 = soup.find_all(class_="accordionPanel")[max-1] # year 3
#   core_modules_section_3 = accordion_panel_3.find(class_="panel-body")
#   module_links_3 = core_modules_section_3.find_all(['h4','p'])
#   module_names_3 = [link.text.strip() for link in module_links_3]
#   module_names_pd_y3['Year 3'] = pd.DataFrame(module_names_3)

#   # print(module_names_pd.iloc[:,0]) #select all rows from column 0
#   module_names_pd = pd.concat([module_names_pd, module_names_pd_y3], axis=1).reset_index(drop=True)
#   # df_year_1 = module_names_pd.iloc[:,0]
#   # df_year_2 = module_names_pd.iloc[:,1]
#   # df_year_3 = module_names_pd_y3['Year 3']
#   # return df_year_1, df_year_2, df_year_3
#   return module_names_pd
# print(creation_df_years(soup, years).iloc[:,2])

def creation_df_years(soup, years):
  module_names_pd = pd.DataFrame()
  module_names_pd_y3 = pd.DataFrame()
  max = len(years) # = 3
  for i in range (0,max): # (0, 1)
      accordion_panel = soup.find_all(class_="accordionPanel")[i]

      # Find the core modules section within the second accordion panel
      if i != max-1: core_modules_section = accordion_panel.find(class_="ds-popbox-content")
      else:          core_modules_section = accordion_panel.find(class_="panel-body")
      # Find all the <h4> and <p> tags within the core modules section
      module_links = core_modules_section.find_all(['h4','p'])

      # Extract the module names
      module_names = [link.text.strip() for link in module_links]
      if i != max-1:
        module_names_pd['Year ',i+1] = pd.DataFrame(module_names)
        module_names_pd = module_names_pd.rename(columns={module_names_pd.columns[i]: f"Year {i+1}"})
      else: 
        module_names_pd_y3['Year 3'] = pd.DataFrame(module_names)

  module_names_pd = pd.concat([module_names_pd, module_names_pd_y3], axis=1).reset_index(drop=True)
  return module_names_pd

# print(creation_df_years(soup, years))

df_year_1 = pd.DataFrame(creation_df_years(soup, years).iloc[:,0])
df_year_2 = pd.DataFrame(creation_df_years(soup, years).iloc[:,1])
df_year_3 = pd.DataFrame(creation_df_years(soup, years).iloc[:,2])
# print(df_year_1.iloc[:,0])

def concat_lines(index1, index2, description_tab):
# Enables to concatenate lines from a tab and insert them 
# in the same position as index 1 into the tab
    concatenated_lines = ' '.join(description_tab[index1:index2])
    description_tab = description_tab[:index1] + description_tab[index2+1:]
    description_tab.insert(index1, concatenated_lines)
    return description_tab

def split_title_description(df_year):
    title_tab = []
    hours_tab = []    
    description_tab = []
    df_year = df_year.fillna('')
    # TODO: remove automatically the sentence skip_line (below) when it occurs 
    # Code does not work, sentence not recognized as the same
    # skip_line = " To learn more about the GSMs offered, click here"
    # df_year = [line for line in df_year if skip_line not in line]
    # if skip_line in df_year:
    #     df_year = df_year.remove(skip_line)
    # df_year = [line for line in df_year if not re.search(re.escape(skip_line), line)]

    for line in df_year: # split title of modules from their description
      # line = line.astype(str)
      # if pd.isna(line):
      #    line = line.fillna('')
      if '[' in line and ']' in line:
          title_tab.append(line)
      elif line == 'General Studies' or line == 'Semestral Projects':
          title_tab.append(line)
      else:
          description_tab.append(line)
    # Remove empty rows in 'description_tab' (isna() does not detect empty lines)
    description_tab = [line for line in description_tab if line]

    # Pattern regex to find "[... hours]" in title_tab
    pattern = r'\[(.*?)\]'
    for i in range(len(title_tab)):
        line = title_tab[i]
        match = re.search(pattern, line)
        if match:
            extracted = match.group(1)  # extract matching part
            hours_tab.append(extracted)
            # Remove this part from each line in title_tab
            title_tab[i] = re.sub(pattern, '', line).strip()

    return title_tab, hours_tab, description_tab

# Year 1 
# print(title_tab)
# skip_line = "To learn more about the GSMs offered, click here"
# for line in df_year_1.iloc[:,0]:
#   if not pd.isna(line):
#     # print((line))
#     if skip_line in line:
       
# print(line)
      # df_year_1.iloc[:,0][line] = df_year_1.iloc[:,0][line].remove(skip_line)
  #   if '[' in line and ']' in line:
  #     print("il y a des crochets sur la ligne")
# print(line)


title_tab = split_title_description(df_year_1.iloc[:,0])[0]
hours_tab = split_title_description(df_year_1.iloc[:,0])[1]
description_tab = split_title_description(df_year_1.iloc[:,0])[2]
description_tab = concat_lines(5,6,description_tab) # append the note that was below the description
description_tab = concat_lines(len(description_tab) - 2, len(description_tab), description_tab)
title_year_1 = pd.DataFrame(title_tab, columns=['title']).to_string(index=False)
hours_year_1 = pd.DataFrame(hours_tab, columns=['hours']).to_string(index=False)
description_year_1 = pd.DataFrame(description_tab, columns=['description']).to_string(index=False)
# year1 = pd.concat([title_year_1, hours_year_1, description_year_1], axis=1)
# print(description_year_1)

# Year 2
# print(df_year_2)
title_tab_2 = split_title_description(df_year_2.iloc[:,0])[0]
hours_tab_2 = split_title_description(df_year_2.iloc[:,0])[1]
description_tab_2 = split_title_description(df_year_2.iloc[:,0])[2]
description_tab_2.insert(title_tab_2.index('Semestral Projects'),'')
hours_tab_2.insert(title_tab_2.index('Semestral Projects'),'')
description_tab_2 = concat_lines(len(description_tab_2) - 2, len(description_tab_2), description_tab_2)
title_year_2 = pd.DataFrame(title_tab_2, columns=['title']).to_string(index=False)
hours_year_2 = pd.DataFrame(hours_tab_2, columns=['hours']).to_string(index=False)
description_year_2 = pd.DataFrame(description_tab_2, columns=['description']).to_string(index=False)
# title_tab_2 = '\n'.join(title_tab_2)
# print(title_year_2)
# print(hours_year_2)
# print(description_year_2)
# -----------------------------------------------------------------------------------------------
# Separate core modules form elective modules for each elective programme (Automation & Robotics Technology | Wafer Fabrication Technology)
index = 0
indexes_core_modules = df_year_3.index[df_year_3['Year 3'].str.contains('Core Modules')] # get the indexes of df_year_3 that contains 'Core Modules' (2 & 26)
indexes_elective_modules = df_year_3.index[df_year_3['Year 3'].str.contains(r'Elective Modules.*', regex=True, case=False)]
# while index <= indexes_core_modules[-1]:
#   print("indexes_core_modules[index+1]",indexes_core_modules[index+1])
#   core_modules = df_year_3[indexes_core_modules[index]:indexes_elective_modules[index]-1]
#   elective_modules = df_year_3[indexes_elective_modules[index]:indexes_core_modules[index+1]-1]

if indexes_core_modules[index] != indexes_core_modules[-1]:
  core_modules_EP_1 = df_year_3[indexes_core_modules[index]:indexes_elective_modules[index]-1]
  elective_modules_EP_1 = df_year_3[indexes_elective_modules[index]:indexes_core_modules[index+1]-1]
  name_EP_1 = df_year_3.iloc[indexes_core_modules[index]-1]
  index=+1
core_modules_EP_2 = df_year_3[indexes_core_modules[index]:indexes_elective_modules[index]-1]
elective_modules_EP_2 = df_year_3[indexes_elective_modules[index]:]
name_EP_2 = df_year_3.iloc[indexes_core_modules[index]-1]
name_EP_1 = ''.join(name_EP_1)
name_EP_2 = ''.join(name_EP_2)
# print(type(name_EP_1))
# print(df_year_3.iloc[indexes_core_modules[index]-1])
# print(type(core_modules_EM_1))
# print(core_modules_EM_1)
# print(elective_modules_EM_1)
# print("elective module 2")
# print(core_modules_EP_2)
# print(elective_modules_EM_2)

# print(core_modules.iloc[:,0]) # to not get the name of column 'Year 3'

# Year 3 (TODO: fix this tab)
title_tab_3_EP_1_CM = split_title_description(core_modules_EP_1.iloc[1:,0])[0]
hours_tab_3_EP_1_CM = split_title_description(core_modules_EP_1.iloc[1:,0])[1]
description_tab_3_EP_1_CM = split_title_description(core_modules_EP_1.iloc[1:,0])[2]
title_year_3_EP_1_CM = pd.DataFrame(title_tab_3_EP_1_CM, columns=['title']).to_string(index=False)
hours_year_3_EP_1_CM = pd.DataFrame(hours_tab_3_EP_1_CM, columns=['hours']).to_string(index=False)
description_year_3_EP_1_CM = pd.DataFrame(description_tab_3_EP_1_CM, columns=['description']).to_string(index=False)
# print(split_title_description(core_modules_EM_1.iloc[1:,0]))
# print(title_year_3_EP_1_CM)
# print(hours_year_3_EP_1_CM)
# print(description_year_3_EP_1_CM)

title_tab_3_EP_1_EM = split_title_description(elective_modules_EP_1.iloc[1:,0])[0]
hours_tab_3_EP_1_EM = split_title_description(elective_modules_EP_1.iloc[1:,0])[1]
description_tab_3_EP_1_EM = split_title_description(elective_modules_EP_1.iloc[1:,0])[2]
title_year_3_EP_1_EM = pd.DataFrame(title_tab_3_EP_1_EM, columns=['title']).to_string(index=False)
hours_year_3_EP_1_EM = pd.DataFrame(hours_tab_3_EP_1_EM, columns=['hours']).to_string(index=False)
description_year_3_EP_1_EM = pd.DataFrame(description_tab_3_EP_1_EM, columns=['description']).to_string(index=False)
# print(title_year_3_EP_1_EM)
# print(hours_year_3_EP_1_EM)
# print(description_year_3_EP_1_EM)

# print("==========================================")

title_tab_3_EP_2_CM = split_title_description(core_modules_EP_2.iloc[1:,0])[0]
hours_tab_3_EP_2_CM = split_title_description(core_modules_EP_2.iloc[1:,0])[1]
description_tab_3_EP_2_CM = split_title_description(core_modules_EP_2.iloc[1:,0])[2]
title_year_3_EP_2_CM = pd.DataFrame(title_tab_3_EP_2_CM, columns=['title']).to_string(index=False)
hours_year_3_EP_2_CM = pd.DataFrame(hours_tab_3_EP_2_CM, columns=['hours']).to_string(index=False)
description_year_3_EP_2_CM = pd.DataFrame(description_tab_3_EP_2_CM, columns=['description']).to_string(index=False)
# print(title_year_3_EP_2_CM)
# print(hours_year_3_EP_2_CM)
# print(description_year_3_EP_2_CM)

title_tab_3_EP_2_EM = split_title_description(elective_modules_EP_2.iloc[1:,0])[0]
hours_tab_3_EP_2_EM = split_title_description(elective_modules_EP_2.iloc[1:,0])[1]
description_tab_3_EP_2_EM = split_title_description(elective_modules_EP_2.iloc[1:,0])[2]
title_year_3_EP_2_EM = pd.DataFrame(title_tab_3_EP_2_EM, columns=['title']).to_string(index=False)
hours_year_3_EP_2_EM = pd.DataFrame(hours_tab_3_EP_2_EM, columns=['hours']).to_string(index=False)
description_year_3_EP_2_EM = pd.DataFrame(description_tab_3_EP_2_EM, columns=['description']).to_string(index=False)
# print(title_year_3_EP_2_EM)
# print(hours_year_3_EP_2_EM)
# print(description_year_3_EP_2_EM)

# skip_line = "To learn more about the GSMs offered, click here"
# if description.iloc[-1]['description'].strip().compare(skip_line.strip()) == 0:
#     # La condition est vérifiée
#     print("La dernière ligne du DataFrame correspond à skip_line.")
# else:
    # La condition n'est pas vérifiée
    # print("La dernière ligne du DataFrame ne correspond pas à skip_line.")
    # print(skip_line)
# print(title_tab_3)




###########

# # Filtrer les lignes contenant '[...]' dans la colonne "Year 3"
# filtered_rows = module_names_pd[module_names_pd.str.contains('\[.*\]')].reset_index(drop=True)

# print(filtered_rows)
# print(filtered_rows.iloc[16,:])
# # Créer une nouvelle dataframe avec les lignes filtrées
# new_dataframe = pd.DataFrame(filtered_rows.str.extract('(\[.*\])'))

# # Afficher la nouvelle dataframe
# print(filtered_rows)
# print('---------------------------------------')
# print(new_dataframe)

# Select programmes from Year 3 :
# accordion_panel = soup.find_all(class_="accordionPanel")[2]
# core_modules_section = accordion_panel.find(class_="panel-body")
# module_links = core_modules_section.find_all(['h4','p'])
# module_names = [link.text.strip() for link in module_links]
# # print(module_names[1]) # Automation & Robotics Technology
# for name in module_names:
#     module_names_pd_y3['Year 3'] = pd.DataFrame(module_names)
# print(module_names_pd_y3)
# # Create new dataframe by concatening dataframe from year1,2 and 3
# final_df = pd.concat([module_names_pd,module_names_pd_y3['Year 3']], axis = 1)
# print(final_df)

# final_df.to_json(r'D:\ESIEE\VOYAGE SINGAP 2023\project\dataframe_programmes_years.json')
# if we want one specific value, i.e. Electrical Principles [60 hours]
# print(final_df.iloc[4][0]) # 4th row, 1st column

# -------------------------------------------------------------------
# """
# Print Career Prospects & Further Studies
categorylist = soup.find(class_="categorylist parbase section")
career_prospects = categorylist.find_all(class_="list-content category-content")
career_prospects_stripped = [link.text.strip() for link in career_prospects]
# for description_career_prospects in career_prospects_stripped:
#      print(description_career_prospects)
# print(career_prospects_stripped[0]) # 0 : career prospects, 1 : further studies
description_career_prospects = career_prospects_stripped[0]
description_further_studies = career_prospects_stripped[1]
description_career_prospects =''.join(description_career_prospects)
description_further_studies = ''.join(description_further_studies)
# -------------------------------------------------------------------

#### Construct the JSON data ####

# nouvelle forme de json #2
# json_data = json.dumps(
# {
#   "fullTimeCourses": [
#     {
#       "name": full_time_course_name,
#       "years": [
#         {
#           "year": 1,
#           "electiveProgrammes": "Name | None",
#           "coreModules": [
#             {
#               "name": "Module Name 1A",
#               "hours": "Hours (or None)",
#               "description": "Module Description 1A"
#             },
#             {
#               "name": "Module Name 1B",
#               "hours": "Hours (or None)",
#               "description": "Module Description 1B"
#             }
#           ],
#           "electiveModules": {
#             "name": "Module Name",
#             "hours": "Hours (or None)",
#             "description": "Module Description"
#           }
#         },
#         {
#           "year": 2,
#           "electiveProgrammes": "Name | None",
#           "coreModules": [
#             {
#               "name": "Module Name 2A",
#               "hours": "Hours (or None)",
#               "description": "Module Description 2A"
#             },
#             {
#               "name": "Module Name 2B",
#               "hours": "Hours (or None)",
#               "description": "Module Description 2B"
#             }
#           ],
#           "electiveModules": {
#             "name": "Module Name",
#             "hours": "Hours (or None)",
#             "description": "Module Description"
#           }
#         },
#         {
#           "year": 3,
#           "electiveProgrammes": "Name | None",
#           "coreModules": [
#             {
#               "name": "Module Name 3A",
#               "hours": "Hours (or None)",
#               "description": "Module Description 3A"
#             },
#             {
#               "name": "Module Name 3B",
#               "hours": "Hours (or None)",
#               "description": "Module Description 3B"
#             }
#           ],
#           "electiveModules": {
#             "name": "Module Name",
#             "hours": "Hours (or None)",
#             "description": "Module Description"
#           }
#         }
#       ]
#     }
#   ],
#   "careerProspects": "Career Prospects Description",
#   "furtherStudies": "Further Studies Description",
#   "contactUs": {
#     "courseManager": {
#       "name": "Manager Name",
#       "telephoneNumber": "Telephone Number",
#       "email": "Email"
#     },
#     "courseCoordinator": {
#       "name": "Coordinator Name",
#       "telephoneNumber": "Telephone Number",
#       "email": "Email"
#     }
#   }
# }, indent = 4)


# nouvelle forme de json #3

year_list = years
# print(year_list)
elective_programmes = []
data = {
    "fullTimeCourses": [
        {
            "name": full_time_course_name,
            "years": []
        }
    ],
    "careerProspects": description_career_prospects,
    "furtherStudies": description_further_studies,
    "contactUs": {
        "courseManager": {
            "name": "Manager Name",
            "telephoneNumber": "Telephone Number",
            "email": "Email"
        },
        "courseCoordinator": {
            "name": "Coordinator Name",
            "telephoneNumber": "Telephone Number",
            "email": "Email"
        }
    }
}

# for year in year_list:
#   if year != 'Year 3':
#     year_data = {
#         "year": year,
#         "core modules": [
#             {
#                 "title": f"{globals()[f'title_year_{year[-1]}']}",
#                 "hours": f"{globals()[f'hours_year_{year[-1]}']}",
#                 "description": f"{globals()[f'description_year_{year[-1]}']}"
#             },
#         ],    
#     }
#   elif year == 'Year 3': 
#     year_data_3 = {
#           "year": year,
#           elective_programmes = [
#             {
#                 "name": name_EP_1, #Automation & Robotics Technology
#                 "core modules": [
#                     {
#                         "title": title_year_3_EP_1_CM,
#                         "hours": hours_year_3_EP_1_CM,
#                         "description": description_year_3_EP_1_CM
#                     },
#                 ],
#                 "elective modules": [
#                     {
#                         "title": title_year_3_EP_1_EM,
#                         "hours": hours_year_3_EP_1_EM,
#                         "description": description_year_3_EP_1_EM
#                     },
#                 ]
#             },
#             {
#                 "name": name_EP_2, #Wafer fabrication technology
#                 "core modules": [
#                     {
#                         "title": title_year_3_EP_2_CM,
#                         "hours": hours_year_3_EP_2_CM,
#                         "description": description_year_3_EP_2_CM
#                     },
#                 ],
#                 "elective modules": [
#                     {
#                         "title": title_year_3_EP_2_EM,
#                         "hours": hours_year_3_EP_2_EM,
#                         "description": description_year_3_EP_2_EM
#                     },
#                 ]
#             }        
#           ]
#     # }
#   # year_data["electiveProgrammes"] = elective_programmes
#   data["fullTimeCourses"][0]["years"].append(year_data)


# print(type(year_data["electiveProgrammes"]))
# print("------------------------------------")
# print(type(data["fullTimeCourses"][0]["years"]))

# Convertir en JSON
## json_data = json.dumps(data, indent=4)
## print(json_data)











for year in year_list:
    if year != 'Year 3':
        year_data = {
            "year": year,
            "core modules": [
                {
                    "title": globals()[f'title_year_{year[-1]}'],
                    "hours": globals()[f'hours_year_{year[-1]}'],
                    "description": globals()[f'description_year_{year[-1]}']
                }
            ]
        }
        data["fullTimeCourses"][0]["years"].append(year_data)
    else:
        year_data_3 = {
            "year": year,
            "elective_programmes": [
                {
                    "name": name_EP_1,
                    "core modules": [
                        {
                            "title": title_year_3_EP_1_CM,
                            "hours": hours_year_3_EP_1_CM,
                            "description": description_year_3_EP_1_CM
                        }
                    ],
                    "elective modules": [
                        {
                            "title": title_year_3_EP_1_EM,
                            "hours": hours_year_3_EP_1_EM,
                            "description": description_year_3_EP_1_EM
                        }
                    ]
                },
                {
                    "name": name_EP_2,
                    "core modules": [
                        {
                            "title": title_year_3_EP_2_CM,
                            "hours": hours_year_3_EP_2_CM,
                            "description": description_year_3_EP_2_CM
                        }
                    ],
                    "elective modules": [
                        {
                            "title": title_year_3_EP_2_EM,
                            "hours": hours_year_3_EP_2_EM,
                            "description": description_year_3_EP_2_EM
                        }
                    ]
                }
            ]
        }
        data["fullTimeCourses"][0]["years"].append(year_data_3)


# with open('test_json.json', 'w') as json_file:
#     json.dump(data, json_file, indent=1)

  
with jsonlines.open('test_jsonl.jsonl', 'w') as json_file:
    json_file.write(data)

driver.quit()


#ancienne forme 

# json_data = json.dumps({
#     "Full time course":full_time_course,  #OK
#     "year":years,                         #OK
#       'Elective programmes': name | none,
#       "core modules": core_modules[[name, hours, description], [name, hours, description], ]
#       "elective modules": elective_modules[[name, hours, description], [name, hours, description], ]
#     "career prospects": description_career_prospects, #OK
#     "further studies": description_further_studies,   #OK
#     "contact us":
        # 'Course manager': {name, telephone number, email},
        # 'Course coordinator': {name, telephone number, email}
# }, indent=4)  # Set indent=4 for pretty formatting


# -----------------------------

# appointments 16 and 23 at 1100 !! check to extract max and raw information if cannot be more precise
# add manually titles...


#### -----------------------------------------------------###
# Use regular expression to extract the desired text 
# (could get "Automation &amp; Robotics Technology")
# match = re.search(r'<h4>\s*([^<>]+)\s*</h4>', html)

# if match:
#     result = match.group(1)
#     print(result)  # Output: Automation & Robotics Technology
# else:
#     print("Text not found in the HTML code.")

####-------------------------------------------------------###

# par flo  

# import requests
# from bs4 import BeautifulSoup

# def scrape_website(url, container_tag, container_specs):
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')

#     for container_class, title_tag, title_class, content_tag in container_specs:
#         container_div = soup.find(container_tag, {'class': container_class})

#         if container_div is None:
#             continue

#         course_titles = container_div.find_all(title_tag, {'class': title_class})
#         course_contents = container_div.find_all(content_tag)

#         for title, content in zip(course_titles, course_contents):
#             print('Title: ', title.get_text())
#             print('Content: ', content.get_text())
#             print()

# # Usage example
# scrape_website(
#     url='https://www.nyp.edu.sg/schools/seg/full-time-courses/robotics-and-mechatronics.html', 
#     container_tag='div', 
#     container_specs=[
#         ('ds-popbox-slide-content ds-popbox-slide_20230511164602760_2', 'h4', 'ds-popbox-slide-content-header', 'p'),
#         ('ds-richtext ds-component-margin', 'h4', 'richtext parbase section', 'p'),  # Assuming no class for title_tag in the second container
#     ]
# )


###----------------------------------------------------------###

# example how to create a simple json file. 
# def write_json(data, filename="NYP_website_test.json"):
#     with open(filename, 'w') as f:
#         json.dump(data, f, indent=4)

# data = ['Bob', "Cindy"]
# write_json(data)"""