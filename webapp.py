import streamlit as st
import google.generativeai as genai
import os
import pandas as pd

api=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api)
model=genai.GenerativeModel('gemini-2.5-flash-lite')

# lets create the UI
st.title(':orange[HEALTHIFY] :- :blue[AI Powered Personel Health Assistant]')

st.markdown('''
            This application will assist you to have a better healthy life. You can ask your
            health related questions and get personalized guidance.
            ''')
tips='''Follow the steps
* Enter your details in the Side bar.
* Enter your Gender, Age, Height (cms), Weight (kgs).
* Select the number on the fitness scale (0 - 5), 5 - Fitness & 0 - No Fitness at all
* After filling the details write your query here and get customized response.'''
st.write(tips)
st.sidebar.header('Enter your Details')
name=st.sidebar.text_input('Enter your Name')
gender=st.sidebar.selectbox('Select your Gender',['Options','Female','Male'])
age=st.sidebar.text_input('Enter your Age')
weight=st.sidebar.text_input('Enter your Weight in kgs')
height=st.sidebar.text_input('Enter your Height in cms')
bmi=pd.to_numeric(weight)/(pd.to_numeric(height)/100)**2
fitness=st.sidebar.slider('Rate your Fitness between 0 - 5',0,5,1)
BMI=st.sidebar.write(f"{name} Your BMI is : {round(bmi,2)} kg/m^2")

# lets use genai model to get the output
user_query=st.text_input('Enter your question here')
prompt=f'''Assume you are a health expert. Your'e required to answer the question asked by the user. 
Use the following details provided by the user.
Name of the user is {name}
Gender is {gender}
Age is {age}
Weight is {weight}
Height is {height}
bmi is {BMI}
user rates his/her fitness as {fitness} out of 5
your output should be in the following format
* It should start by giving one or two line comment on the details that have been provided.
* It should explain what is the real problem based on the query asked by user.
* What could be the possible reason for the problem.
* What are the possible solutions for the problem.
* You can also mention what doctor to see (specilization) if required.
* Strictly do not recommend or advice any medicine rather than home remedies
* Output should be in bullet points and use tables wherever required

here is the query from the user {user_query}'''
if user_query:
    response=model.generate_content(prompt)
    st.write(response.text)