import os  # Importing the 'os' module to access operating system functionalities
from apikey import apikey  # Importing the 'apikey' from a separate file

import streamlit as st  # Importing the 'streamlit' library and assigning it the alias 'st'
from langchain.llms import OpenAI  # Importing the 'OpenAI' class from 'llms' module in 'langchain' package
from langchain.prompts import PromptTemplate  # Importing the 'PromptTemplate' class from 'prompts' module in 'langchain' package
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain  # Importing classes from 'chains' module in 'langchain' package
from langchain.memory import ConversationBufferMemory  # Importing the 'ConversationBufferMemory' class from 'memory' module in 'langchain' package

os.environ['OPENAI_API_KEY'] = apikey  # Setting the 'OPENAI_API_KEY' environment variable using the 'apikey' value

# App Framework
st.title('◘ ◘ LangChain Tutorial')  # Setting the title of the Streamlit application to '◘ ◘ LangChain Tutorial'
prompt = st.text_input('♣ •Type your query: •')  # Creating a text input field in the Streamlit application for user input

# Prompt template
title_template = PromptTemplate(
    input_variables=['topic'],  # Defining input variables for the 'title_template' prompt template
    template='Generate a python code for {topic}'  # Defining a template for the 'title_template' prompt template
)

infornmation_template = PromptTemplate(
    input_variables=['title'],  # Defining input variables for the 'infornmation_template' prompt template
    template='how does the {title} work and explain in detail'  # Defining a template for the 'infornmation_template' prompt template
)

# Memory
memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')  # Creating a ConversationBufferMemory object with specified input and memory keys

# LLMS
llm = OpenAI(temperature=0.9)  # Creating an OpenAI object with a temperature value of 0.9
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, memory=memory, output_key='title')  # Creating an LLMChain object with specified parameters
information_chain = LLMChain(llm=llm, prompt=infornmation_template, verbose=True, memory=memory, output_key='info')  # Creating an LLMChain object with specified parameters

seq_chain = SequentialChain(chains=[title_chain, information_chain], verbose=True, input_variables=['topic'], output_variables=['title', 'info'])  # Creating a SequentialChain object with specified chains and parameters

# Print response of the prompt on the screen
if prompt:
    response1 = title_chain.run(topic=prompt)  # Running the 'title_chain' LLMChain with the user's input as the 'topic' parameter
    response2 = seq_chain({'topic': prompt})  # Running the 'seq_chain' SequentialChain with the user's input as the 'topic' parameter
    st.write(response1)  # Displaying the response of 'title_chain' on the Streamlit application
    st.write("=========================== WORKING and MORE INFO. ===============================")  # Displaying a separator
    st.write(response2)  # Displaying the response of 'seq_chain' on the Streamlit application

    with st.expander('Memory History'):  # Creating an expandable section in the Streamlit application
        st.info(memory.buffer)  # Displaying the contents of the memory buffer in the expandable section
