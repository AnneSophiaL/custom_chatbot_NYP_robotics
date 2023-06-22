# import json
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select

# # Set up Selenium webdriver
# driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed and its location in PATH
# driver.get("https://www.nyp.edu.sg/schools/seg/full-time-courses/robotics-and-mechatronics.html")

# # Wait for the dropdown menus to load
# year1_dropdown = Select(driver.find_element_by_id("yui_patched_v3_11_0_1_1622408252046_228"))
# year2_dropdown = Select(driver.find_element_by_id("yui_patched_v3_11_0_1_1622408252046_229"))
# year3_dropdown = Select(driver.find_element_by_id("yui_patched_v3_11_0_1_1622408252046_230"))

# # Get the available options from each dropdown
# year1_options = [option.text for option in year1_dropdown.options]
# year2_options = [option.text for option in year2_dropdown.options]
# year3_options = [option.text for option in year3_dropdown.options]

# # Store options in a dictionary
# data = {
#     "Year 1": year1_options,
#     "Year 2": year2_options,
#     "Year 3": year3_options
# }

# # Save data to a JSON file
# with open("dropdown_options.json", "w") as json_file:
#     json.dump(data, json_file, indent=4)

# # Quit the browser
# driver.quit()

import json
from selenium import webdriver
from selenium.webdriver.common.by import By


# Set up Selenium webdriver
driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed and its location in PATH
driver.get("https://www.nyp.edu.sg/schools/seg/full-time-courses/robotics-and-mechatronics.html")

driver.execute_script("""document.querySelector("select[name='date1'] option").value="2016-09-07";""")
# Wait for the dropdown menus to load
# year1_dropdown = driver.find_element(By.XPATH, "//*[@id=\"nypaiwpCoursesList_accordion_9ed06ee9-53b6-4652-982e-e46fb0db156f\"]/div[1]/div[2]")
# year2_dropdown = driver.find_element(By.XPATH, "//*[@id=\"nypaiwpCoursesList_accordion_9ed06ee9-53b6-4652-982e-e46fb0db156f\"]/div[2]/div[2]")
# year3_dropdown = driver.find_element(By.XPATH, "//*[@id=\"nypaiwpCoursesList_accordion_9ed06ee9-53b6-4652-982e-e46fb0db156f\"]/div[3]/div[2]")


modules_elements = driver.find_elements(By.CLASS_NAME, 'par0_1543561249985')
# modules_classyear2 = driver.find_elements(By.CLASS_NAME, 'desc-title') # print : year 1 ; year 2 ; year 3 

modules2 = driver.find_elements(By.CLASS_NAME, '#nypaiwpCoursesList_accordion_9ed06ee9-53b6-4652-982e-e46fb0db156f > div:nth-child(1) > div.accordion.accordionPanelContent_accordion_9ed06ee9-53b6-4652-982e-e46fb0db156f_0.collapse.in')



# modules_elements_2 = driver.find_elements(By.CLASS_NAME, 'nypai-sListing')  

modules_texts = [element.text for element in modules2]
#nypaiwpCoursesList_accordion_9ed06ee9-53b6-4652-982e-e46fb0db156f > div:nth-child(1) > div.accordion.accordionPanelContent_accordion_9ed06ee9-53b6-4652-982e-e46fb0db156f_0.collapse.in
# modules_classyear2 = [element.text for element in modules_classyear2]

# # Get the available options from each dropdown
# year1_options = [option.text for option in year1_dropdown.find_elements_by_tag_name("option")]
# year2_options = [option.text for option in year2_dropdown.find_elements_by_tag_name("option")]
# year3_options = [option.text for option in year3_dropdown.find_elements_by_tag_name("option")]

print(modules_texts)


# # Store options in a dictionary
# data = {
#     "Year 1": year1_options,
#     "Year 2": year2_options,
#     "Year 3": year3_options
# }

# # Save data to a JSON file
# with open("dropdown_options.json", "w") as json_file:
#     json.dump(data, json_file, indent=4)

# Quit the browser
driver.quit()
