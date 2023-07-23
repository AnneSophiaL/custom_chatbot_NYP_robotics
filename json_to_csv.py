import pandas as pd
from pandas import json_normalize
import json

# Specify the path to your JSON file
json_file_path = 'D:\ESIEE\VOYAGE SINGAP 2023\project_custom_chatbot_nyp\EWB.json'

# Read the JSON file
with open(json_file_path, encoding='utf-8') as f:
    json_data = json.load(f)


# Load the data
# json_data = json.loads(data)
courses = json_data['fullTimeCourses']

# Initialize lists to store DataFrames
dfs = []

# Iterate through each course
for course in courses:
    years = course.pop('years')  # Remove the 'years' field and store it in a separate variable
    # # Iterate through each year
    for year in years:
        if year != years[2]:
            modules = year.pop('core modules')  # Remove the 'core modules' field and store it in a separate variable
            # print(modules)
            # print("===================================================")
        # if year == years[2]:
        #     modules_year_3=year.pop('modules')
        #     # print(modules_year_3)
        #     for module in modules_year_3:
        #         core_module = module.pop('core modules')
        #         elective_module = module.pop('elective modules')
    #     # Iterate through each module
        for module in modules:
            df = pd.json_normalize({**course, **year, **module})  # Merge all dictionaries and normalize to a DataFrame
            dfs.append(df)

# # Use pandas json_normalize function to flatten the data
# df = pd.json_normalize(data, record_path=['modules', 'core modules'], meta=['year'])
# df2 = pd.json_normalize(data, record_path=['modules', 'elective modules'], meta=['year'])

# Concatenate the two dataframes
# final_df = pd.concat([df, df2], axis=0).reset_index(drop=True)




# # Concatenate all DataFrames
result = pd.concat(dfs, ignore_index=True)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(result)




# # Save to a CSV file
# result.to_csv('output.xlsx', index=False)