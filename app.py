import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.memory import ConversationBufferMemory

os.environ['OPENAI_API_KEY'] = apikey

#App FrameWork
st.title('◘ ◘ LangChain Tutorial')
prompt = st.text_input('♣ •Type your query: •')

#Prompt template
title_template = PromptTemplate(
    input_variables = ['topic'],
    template = 'Generate a python code for {topic}'
    )

infornmation_template = PromptTemplate(
    input_variables = ['title'],
    template = 'how does the {title} work and explain in detail'
    )

#Memory
memory = ConversationBufferMemory(input_key= 'topic', memory_key= 'chat_history')

#LLMS
llm = OpenAI(temperature = 0.9)
title_chain = LLMChain(llm = llm, prompt = title_template, verbose= True, memory=memory, output_key='title')
information_chain = LLMChain(llm = llm, prompt = infornmation_template, verbose= True, memory= memory, output_key='info')

seq_chain = SequentialChain(chains = [title_chain, information_chain], verbose= True, input_variables=['topic'], output_variables=['title','info'])

#Print response of the prompt on the screen
if prompt:
    response1 = title_chain.run(topic = prompt)
    response2 = seq_chain({'topic': prompt})
    st.write(response1)
    st.write("=========================== WORKING and MORE INFO. ===============================")
    st.write(response2)

    with st.expander('Memory History'):
        st.info(memory.buffer)