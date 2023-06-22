# pip install beautifulsoup4, 
# pip install parser-libraries
# pip install requests

# download Chromedriver : 
# Go to https://chromedriver.chromium.org/downloads and download the chromedriver according to your Chrome version
# to see your Chrome version, go to 'Help' and 'About Google Chrome'
# Mine is : Version 113.0.5672.93 so I choose version 113.  

# from bs4 import BeautifulSoup
# from urllib.request import *
from selenium import webdriver 
from selenium.webdriver.common.by import By
# import requests

# url = "https://www.nyp.edu.sg/schools/seg/full-time-courses/robotics-and-mechatronics.html"
# PATH = 'D:\ESIEE\VOYAGE SINGAP 2023\project\Chromedriver'
# driver = webdriver.Chrome(PATH)
# driver.get(url)

# ---------------------------------------------------------------
# get the core modules of year 1 (Algebra, Calculus, Effective Communication Skills...)
# if only get names of modules : class = nypai-sListing

# test = driver.find_element(By.CLASS_NAME, "panel-body").text
# print(test[1])

# ---------------------------------------------------------------
# ---------------------------------------------------------------


# code that comes from :"https://www.geeksforgeeks.org/convert-html-source-code-to-json-object-using-python/"

import xmltojson
import json
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


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
with open("NYP_robotics.html", "w", encoding='utf8') as html_file:
	html_file.write(driver.page_source)
	
# with open("NYP_robotics.html", "r", encoding='utf8') as html_file:
#     html = html_file.read()
#     # Use Selenium to extract all elements from the HTML
#     elements = driver.find_elements("//*")  # Find all elements regardless of tag name

#     # Extract the text content of each element
#     element_texts = [element.text for element in elements]

#     # Convert the extracted data to JSON
#     json_data = json.dumps(element_texts)

#     # Save the JSON data to a file
#     with open("NYP_robotics.json", "w", encoding='utf8') as file:
#         file.write(json_data)
	
# ----------------------------------------------------
with open("NYP_robotics.html", "r", encoding='utf8') as html_file:
    html = html_file.read()
    ### -----------------------------------------------------

    # tried to select only the course titles but did not work (several repetition of same data)

    # Use Selenium to extract elements from the HTML
    headings = driver.find_elements(By.TAG_NAME, 'h1')  # Extract elements with tag name <h1>
    h4_elements = driver.find_elements(By.TAG_NAME, 'h4')  # Extract elements with tag name <h4>
    a_elements = driver.find_elements(By.TAG_NAME, 'a')  # Extract elements with tag name <a>
    div_elements = driver.find_elements(By.TAG_NAME, 'div') # Extract elements with tag name <div>
    modules_elements = driver.find_elements(By.CLASS_NAME, 'nypai-sListing') #should be all the courses names, only year 1 is displayed 
    modules_names_elements = driver.find_elements(By.CLASS_NAME, 'desc-title')  
    

    # Extract the text content of each element
    # heading_texts = [heading.text for heading in headings]
    # h4_texts = [element.text for element in h4_elements]
    # a_texts = [element.text for element in a_elements]
    # div_texts = [element.text for element in div_elements]
    modules_texts = [element.text for element in modules_elements]
    modules_names_texts = [element.text for element in modules_names_elements]


    # Convert the extracted data to JSON
    json_data = json.dumps({
        # "headings": heading_texts,
        # "h4_elements": h4_texts,
        # "a_elements": a_texts,
        # "div_elements": div_texts,
        "names of modules":modules_names_texts,
        "modules": modules_texts
    }, indent=4)  # Set indent=4 for pretty formatting
    ### -----------------------------------------------------

    # # did not work
    # # Use Selenium to extract elements from the HTML
    # course_title_element = driver.find_element(By.CSS_SELECTOR, 'h1.course-title')  # Extract course title
    # about_element = driver.find_element(By.CSS_SELECTOR, '.course-about')  # Extract about section
    # modules_elements = driver.find_elements(By.CSS_SELECTOR, '.course-modules h4')  # Extract module headings

    # # Extract the text content of each element
    # course_title = course_title_element.text.strip()
    # about_text = about_element.text.strip()
    # modules = [element.text.strip() for element in modules_elements]

    # # Construct the JSON data
    # json_data = json.dumps({
    #     "course_title": course_title,
    #     "about": about_text,
    #     "modules": modules
    # }, indent=4)  # Set indent=4 for pretty formatting

    ### -----------------------------------------------------------
	
with open("NYP_robotics.json", "w", encoding='utf8') as file:
	json.dump(json_data, file)
	
# print(json_data)

# Quit the driver
driver.quit()
