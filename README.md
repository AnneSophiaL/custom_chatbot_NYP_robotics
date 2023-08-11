# custom_chatbot_NYP_robotics

This project is a vocal chatbot that can listen to a user's question and tell the response verbally. I used Streamlit as a graphical user interface.

The files that are working are "test_custom_chatbot_1.ipynb" and "test_custom_chatbot_2.ipynb" for any tests. 
"test_custom_chatbot_5.ipynb" is also working but does not have any training, it is a simple chatbot.


The "webscraping_EWB.py" and "webscraping_RM.py" files are used to collect the data from the NYP website's pages:
- https://www.nyp.edu.sg/schools/seg/full-time-courses/robotics-and-mechatronics.html 
- https://www.nyp.edu.sg/schools/seg/full-time-courses/engineering-with-business.html 

The folder "my_data" contains all of my dataset, the files inside are text files, xlsx files and json files. For now, any other types of file are supported but csv files. 

The "app.py" file is the main python file that should be run using the command "streamlit run app.py"

There is a "questions_chatbot.txt" file that contains questions for testing the chatbot, it is composed of 20 questions but onthers can be added. 