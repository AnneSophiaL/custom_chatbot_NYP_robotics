import json
from bs4 import BeautifulSoup
import re
import pandas as pd
import jsonlines
import requests

url = "https://www.nyp.edu.sg/schools/seg/full-time-courses/robotics-and-mechatronics.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# -------------------------------------------------------------------
full_time_course_name = soup.find('title').text.strip() # Diploma in Robotics & Mechatronics

years = soup.find_all(text=lambda text: text and 'Year' in text) # ['Year 1', 'Year 2', 'Year 3']

# about the course
info = soup.find(class_="list-content col-lg-12")
info = info.find(class_="ds-richtext")
info = info.find_all(['h4','p'])
info = [link.text.strip() for link in info if link.text.strip() != '']
info = " ".join(info)

# -------------------------------------------------------------------
# contact us course manager
contact = soup.find(class_="nypContactItemLeft")
contact = contact.find_all(['h3', 'p'])
contact = [link.text.strip() for link in contact]

# contact us course coordinators
coord = soup.find(class_="nypContactItemRight")
coord = coord.find_all(['h3', 'p'])
coord = [link.text.strip() for link in coord]

def creation_df_years(soup, years):
  module_names_pd = pd.DataFrame()
  module_names_pd_y3 = pd.DataFrame()
  max = len(years) # = 3
  for i in range (0,max): # (0, 1, 2)
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

# Creation of 3 Dataframe for each year
df_year_1 = pd.DataFrame(creation_df_years(soup, years).iloc[:,0])
df_year_2 = pd.DataFrame(creation_df_years(soup, years).iloc[:,1])
df_year_3 = pd.DataFrame(creation_df_years(soup, years).iloc[:,2])

# print(df_year_1)
YEAR_1 = pd.DataFrame()
YEAR_2 = pd.DataFrame()
YEAR_3 = pd.DataFrame()


def concat_lines(index1, index2, description_tab):
# Enables to concatenate lines from a tab and insert them in the same position as index 1 into the tab
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

# -----------------------------------------------------------------------------------------------

# Year 1 
title_tab_1 = split_title_description(df_year_1.iloc[:,0])[0]
hours_tab_1 = pd.DataFrame(split_title_description(df_year_1.iloc[:,0])[1])
empty_row = pd.Series('', index=hours_tab_1.columns)
hours_tab_1 = hours_tab_1.append(empty_row, ignore_index=True)
description_tab_1 = split_title_description(df_year_1.iloc[:,0])[2]
description_tab_1 = concat_lines(5,6,description_tab_1) # append the note that was below the description
description_tab_1 = concat_lines(len(description_tab_1) - 2, len(description_tab_1), description_tab_1)

YEAR_1['title'] = title_tab_1
YEAR_1['hours'] = hours_tab_1
YEAR_1['description'] = description_tab_1
# print(YEAR_1)
# Year 2
title_tab_2 = split_title_description(df_year_2.iloc[:,0])[0]
hours_tab_2 = split_title_description(df_year_2.iloc[:,0])[1]
hours_tab_2.insert(title_tab_2.index('Semestral Projects'), '')
hours_tab_2 = pd.DataFrame(hours_tab_2)
empty_row = pd.Series('', index=hours_tab_2.columns)
hours_tab_2 = hours_tab_2.append(empty_row, ignore_index=True)
description_tab_2 = split_title_description(df_year_2.iloc[:,0])[2]
description_tab_2.insert(title_tab_2.index('Semestral Projects'),'')
description_tab_2 = concat_lines(len(description_tab_2) - 2, len(description_tab_2), description_tab_2)
YEAR_2['title'] = title_tab_2
YEAR_2['hours'] = hours_tab_2
YEAR_2['description'] = description_tab_2
# print(YEAR_2)

# Year 3 
# Separate core modules form elective modules for each elective programme (Automation & Robotics Technology | Wafer Fabrication Technology)
# I first get the indexes of each separate points
index = 0
indexes_core_modules = df_year_3.index[df_year_3['Year 3'].str.contains('Core Modules')] # get the indexes of df_year_3 that contains 'Core Modules' (2 & 26)
indexes_elective_modules = df_year_3.index[df_year_3['Year 3'].str.contains(r'Elective Modules.*', regex=True, case=False)]

if indexes_core_modules[index] != indexes_core_modules[-1]:
  core_modules_EP_1 = df_year_3[indexes_core_modules[index]:indexes_elective_modules[index]-1]
  elective_modules_EP_1 = df_year_3[indexes_elective_modules[index]:indexes_core_modules[index+1]-1]
  name_EP_1 = df_year_3.iloc[indexes_core_modules[index]-1]
  index=+1
core_modules_EP_2 = df_year_3[indexes_core_modules[index]:indexes_elective_modules[index]-1]
elective_modules_EP_2 = df_year_3[indexes_elective_modules[index]:]
name_EP_2 = df_year_3.iloc[indexes_core_modules[index]-1]
# print(type(elective_modules_EP_2.iloc[5]))
# print(type(name_EP_2))
# get the names of the elective programmes
name_EP_1 = ''.join(name_EP_1)
name_EP_2 = ''.join(name_EP_2)

# elective programme 1 : automation & robotics technology core module and elective module
title_tab_3_EP_1_CM = split_title_description(core_modules_EP_1.iloc[1:,0])[0]
hours_tab_3_EP_1_CM = pd.DataFrame(split_title_description(core_modules_EP_1.iloc[1:,0])[1])
empty_row = pd.Series('', index=hours_tab_3_EP_1_CM.columns)
hours_tab_3_EP_1_CM = hours_tab_3_EP_1_CM.append(empty_row, ignore_index=True)
description_tab_3_EP_1_CM = split_title_description(core_modules_EP_1.iloc[1:,0])[2]

core_modules_YEAR_3 = pd.DataFrame()
core_modules_YEAR_3['title'] = title_tab_3_EP_1_CM
core_modules_YEAR_3['hours'] = hours_tab_3_EP_1_CM
core_modules_YEAR_3['description'] = description_tab_3_EP_1_CM
# print(core_modules_YEAR_3)

title_tab_3_EP_1_EM = split_title_description(elective_modules_EP_1.iloc[1:,0])[0]
hours_tab_3_EP_1_EM = pd.DataFrame(split_title_description(core_modules_EP_1.iloc[1:,0])[1])
empty_row = pd.Series('', index=hours_tab_3_EP_1_EM.columns)
hours_tab_3_EP_1_EM = hours_tab_3_EP_1_EM.append(empty_row, ignore_index=True)
description_tab_3_EP_1_EM = split_title_description(elective_modules_EP_1.iloc[1:,0])[2]

elective_modules_YEAR_3 = pd.DataFrame()
elective_modules_YEAR_3['title'] = title_tab_3_EP_1_EM
elective_modules_YEAR_3['hours'] = hours_tab_3_EP_1_EM
elective_modules_YEAR_3['description'] = description_tab_3_EP_1_EM
# print(elective_modules_YEAR_3)

YEAR_3_1 = pd.concat([core_modules_YEAR_3, elective_modules_YEAR_3], axis=1, names=['core modules', 'elective modules'])
print(YEAR_3_1)

# elective programme 2 : Wafer Fabrication Technology core module and elective module
title_tab_3_EP_2_CM = split_title_description(core_modules_EP_2.iloc[1:,0])[0]
hours_tab_3_EP_2_CM = pd.DataFrame(split_title_description(core_modules_EP_2.iloc[1:,0])[1])
empty_row = pd.Series('', index=hours_tab_3_EP_2_CM.columns)
hours_tab_3_EP_2_CM = hours_tab_3_EP_2_CM.append(empty_row, ignore_index=True)
description_tab_3_EP_2_CM = split_title_description(core_modules_EP_2.iloc[1:,0])[2]

core_modules_YEAR_3 = pd.DataFrame()
core_modules_YEAR_3['title'] = title_tab_3_EP_2_CM
core_modules_YEAR_3['hours'] = hours_tab_3_EP_2_CM
core_modules_YEAR_3['description'] = description_tab_3_EP_2_CM

title_tab_3_EP_2_EM = split_title_description(elective_modules_EP_2.iloc[1:,0])[0]
hours_tab_3_EP_2_EM = pd.DataFrame(split_title_description(elective_modules_EP_2.iloc[1:,0])[1])
empty_row = pd.Series('', index=hours_tab_3_EP_2_EM.columns)
hours_tab_3_EP_2_EM = hours_tab_3_EP_2_EM.append(empty_row, ignore_index=True)
description_tab_3_EP_2_EM = split_title_description(elective_modules_EP_2.iloc[1:-1,0])[2]
# print(description_tab_3_EP_2_EM)

elective_modules_YEAR_3 = pd.DataFrame()
elective_modules_YEAR_3['title'] = title_tab_3_EP_2_EM
elective_modules_YEAR_3['hours'] = hours_tab_3_EP_2_EM
elective_modules_YEAR_3['description'] = description_tab_3_EP_2_EM

YEAR_3_2 = pd.concat([core_modules_YEAR_3, elective_modules_YEAR_3], axis=1, names=['core modules', 'elective modules'])
# print(YEAR_3_2)
YEAR_3 = pd.concat([YEAR_3_1, YEAR_3_2], keys=['automation and robotics technology', 'wafer fabrication technology'])
# print(YEAR_3)
# -----------------------------------------------------------------------------------------------
# YEARS = pd.DataFrame()
# YEARS = pd.concat([YEAR_1, YEAR_2, YEAR_3], keys=['Year 1', 'Year 2', 'Year 3'])
# print(YEARS)
YEAR_1.to_csv('YEAR_1.csv', index=False)
YEAR_2.to_csv('YEAR_2.csv', index=False)
YEAR_3.to_csv('YEAR_3.csv', index=False)

# -----------------------------------------------------------------------------------------------

# Print Career Prospects & Further Studies
categorylist = soup.find(class_="categorylist parbase section")
career_prospects = categorylist.find_all(class_="list-content category-content")
career_prospects_stripped = [link.text.strip() for link in career_prospects]
description_career_prospects = career_prospects_stripped[0]
description_further_studies = career_prospects_stripped[1]
description_career_prospects =''.join(description_career_prospects)
description_further_studies = ''.join(description_further_studies)

# -------------------------------------------------------------------

#### Construction of the JSON data ####

# year_list = years
# elective_programmes = []
# data = {
#     "fullTimeCourses": [
#         {
#             "name": full_time_course_name,
#             "about the course": info,
#             "years": []
#         }
#     ],
#     "career Prospects": description_career_prospects,
#     "further Studies": description_further_studies,
#     "contact Us": {
#         "course Manager": {
#             "name": contact[1],
#             "telephone Number": contact[2],
#             "email": contact[3]
#         },
#         "course Coordinator": [
#             {
#                 "name": coord[1],
#                 "telephone Number": coord[2],
#                 "email": coord[3]
#             },
#             {
#                 "name": coord[5],
#                 "telephone Number": coord[6],
#                 "email": coord[7]
#             }
#         ]
#     }

# }

# for year in year_list:
#     if year != 'Year 3':
#         year_data = {
#             "year": year,
#             "core modules": [
#                 {
#                     "title": globals()[f'title_tab_{year[-1]}'],
#                     "hours": globals()[f'hours_tab_{year[-1]}'],
#                     "description": globals()[f'description_tab_{year[-1]}']
#                 }
#             ]
#         }
#         data["fullTimeCourses"][0]["years"].append(year_data)
#     else:
#         year_data_3 = {
#             "year": year,
#             "elective_programmes": [
#                 {
#                     "name": name_EP_1,
#                     "core modules": [
#                         {
#                             "title": title_tab_3_EP_1_CM,
#                             "hours": hours_tab_3_EP_1_CM,
#                             "description": description_tab_3_EP_1_CM
#                         }
#                     ],
#                     "elective modules": [
#                         {
#                             "title": title_tab_3_EP_1_EM,
#                             "hours": hours_tab_3_EP_1_EM,
#                             "description": description_tab_3_EP_1_EM
#                         }
#                     ]
#                 },
#                 {
#                     "name": name_EP_2,
#                     "core modules": [
#                         {
#                             "title": title_tab_3_EP_2_CM,
#                             "hours": hours_tab_3_EP_2_CM,
#                             "description": description_tab_3_EP_2_CM
#                         }
#                     ],
#                     "elective modules": [
#                         {
#                             "title": title_tab_3_EP_2_EM,
#                             "hours": hours_tab_3_EP_2_EM,
#                             "description": description_tab_3_EP_2_EM
#                         }
#                     ]
#                 }
#             ]
#         }
#         data["fullTimeCourses"][0]["years"].append(year_data_3)


# with open('R&M.json', 'w') as json_file:
#     json.dump(data, json_file, indent=1)

# if we want a jsonl file:
# with jsonlines.open('R&M.jsonl', 'w') as json_file:
#     json_file.write(data)