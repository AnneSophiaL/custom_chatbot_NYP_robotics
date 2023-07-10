import json
from bs4 import BeautifulSoup
import re
import pandas as pd
import jsonlines
import requests 

url = "https://www.nyp.edu.sg/schools/seg/full-time-courses/engineering-with-business.html"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# -------------------------------------------------------------------
full_time_course_name = soup.find('title').text.strip() # Diploma in Engineering with Business

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

# contact us course coordinator
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

# Convert into DataFrame for each year
df_year_1 = pd.DataFrame(creation_df_years(soup, years).iloc[:,0])
df_year_2 = pd.DataFrame(creation_df_years(soup, years).iloc[:,1])
df_year_3 = pd.DataFrame(creation_df_years(soup, years).iloc[:,2])

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

###### Year 1
# Separate info into 3 DataFrames : Title, Hours, Desccription
title_tab = split_title_description(df_year_1.iloc[:,0])[0]
hours_tab = split_title_description(df_year_1.iloc[:,0])[1]
description_tab = split_title_description(df_year_1.iloc[:,0])[2]
description_tab = concat_lines(5,6,description_tab) # append the note that was below the description
description_tab = concat_lines(len(description_tab) - 2, len(description_tab), description_tab)
title_year_1 = pd.DataFrame(title_tab, columns=['title']).to_string(index=False)
hours_year_1 = pd.DataFrame(hours_tab, columns=['hours']).to_string(index=False)
description_year_1 = pd.DataFrame(description_tab, columns=['description']).to_string(index=False)

###### Year 2
# Separate info into 3 DataFrames : Title, Hours, Desccription
title_tab_2 = split_title_description(df_year_2.iloc[:,0])[0]
hours_tab_2 = split_title_description(df_year_2.iloc[:,0])[1]
description_tab_2 = split_title_description(df_year_2.iloc[:,0])[2]
description_tab_2 = concat_lines(len(description_tab_2) - 2, len(description_tab_2), description_tab_2)
title_year_2 = pd.DataFrame(title_tab_2, columns=['title']).to_string(index=False)
hours_year_2 = pd.DataFrame(hours_tab_2, columns=['hours']).to_string(index=False)
description_year_2 = pd.DataFrame(description_tab_2, columns=['description']).to_string(index=False)

###### Year 3
# Separate Core modules and Elective modules
index = 0
indexes_core_modules = df_year_3.index[df_year_3['Year 3'].str.contains('Core Modules')  & (df_year_3['Year 3'] != '')] # get the indexes of df_year_3 that contains 'Core Modules' (2 & 26)
indexes_elective_modules = df_year_3.index[df_year_3['Year 3'].str.contains(r'Elective Modules.*', regex=True, case=False)  & (df_year_3['Year 3'] != '')]
core_modules = df_year_3[indexes_core_modules[index]:indexes_elective_modules[index]-1]
elective_modules = df_year_3[indexes_elective_modules[index]:]

# Separate info into 6 DataFrames : Title, Hours, Desccription for core and elective modules
title_tab_3_CM = split_title_description(core_modules.iloc[1:,0])[0]
hours_tab_3_CM = split_title_description(core_modules.iloc[1:,0])[1]
description_tab_3_CM = split_title_description(core_modules.iloc[1:,0])[2]
title_year_3_CM = pd.DataFrame(title_tab_3_CM, columns=['title']).to_string(index=False)
hours_year_3_CM = pd.DataFrame(hours_tab_3_CM, columns=['hours']).to_string(index=False)
description_year_3_CM = pd.DataFrame(description_tab_3_CM, columns=['description']).to_string(index=False)

title_tab_3_EM = split_title_description(elective_modules.iloc[1:,0])[0]
hours_tab_3_EM = split_title_description(elective_modules.iloc[1:,0])[1]
description_tab_3_EM = split_title_description(elective_modules.iloc[1:,0])[2]
title_year_3_EM = pd.DataFrame(title_tab_3_EM, columns=['title']).to_string(index=False)
hours_year_3_EM = pd.DataFrame(hours_tab_3_EM, columns=['hours']).to_string(index=False)
description_year_3_EM = pd.DataFrame(description_tab_3_EM, columns=['description']).to_string(index=False)

# -------------------------------------------------------------------

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

#### Construction of the JSON data ####

year_list = years
elective_programmes = []
data = {
    "fullTimeCourses": [
        {
            "name": full_time_course_name,
            "about the course": info,
            "years": []
        }
    ],
    "career Prospects": description_career_prospects,
    "further Studies": description_further_studies,
    "contact Us": {
        "course Manager": {
            "name": contact[1],
            "telephone Number": contact[2],
            "email": contact[3]
        },
        "course Coordinator": [
            {
                "name": coord[1],
                "telephone Number": coord[2],
                "email": coord[3]
            }
        ]
    }

}

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
        "modules": [
            {
                "core modules": [
                    {
                        "title": title_year_3_CM,
                        "hours": hours_year_3_CM,
                        "description": description_year_3_CM
                    }
                ],
                "elective modules": [
                    {
                        "title": title_year_3_EM,
                        "hours": hours_year_3_EM,
                        "description": description_year_3_EM
                    }
                ]
            }
        ]
    }
        data["fullTimeCourses"][0]["years"].append(year_data_3)


with open('EWB.json', 'w') as json_file:
    json.dump(data, json_file, indent=1)

# if we want in jsonl file:
# with jsonlines.open('EWB.jsonl', 'w') as json_file:
#     json_file.write(data)

driver.quit()
