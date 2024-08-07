import os
from dotenv import load_dotenv
load_dotenv()
from bs4 import BeautifulSoup

from flask import Flask, jsonify, request, send_file, redirect,has_request_context,make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import json
import base64
import datetime
import random
import string
import uuid
import mysql.connector

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.agent_toolkits import create_sql_agent
from langchain_core.pydantic_v1 import BaseModel, Field

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
model = ChatOpenAI()
parser = StrOutputParser()
embeddings = OpenAIEmbeddings()

tagging_prompt = ChatPromptTemplate.from_template(
    """
    Extract the desired information from the following passage.

    Only extract the properties mentioned in the 'Classification' function.

    Passage:
    {input}
    """
    )

class Classification(BaseModel):
    sentiment: str = Field(description="The sentiment of the text")
    aggressiveness: int = Field(description="How aggressive the text is on a scale from 1 to 10")
    language: str = Field(description="The language the text is written in")

# dbhost = os.getenv('HOST')
# dbuser = os.getenv('DBUSER')
# dbpassword = os.getenv('DBPASSWORD')
# database = os.getenv('DATABASE')

app = Flask(__name__)
limiter = Limiter(get_remote_address,app=app,default_limits=["1000 per day", "100 per hour"])

@app.route('/lang_chain_api/simple_llm_call',methods=['GET','POST'])
def simple_llm_call_api():

    some_json = request.get_json()
    query = some_json['query']
    
    response = model.invoke(query)
    output = {"response": response.content}

    return jsonify(output)

@app.route('/lang_chain_api/llm_call_with_prompt',methods=['GET','POST'])
def llm_call_with_prompt_api():

    some_json = request.get_json()
    template = some_json['template']
    fields = some_json['fields']
    number_of_fields = len(fields)+1

    field_dict = {}
    for i in range(1,number_of_fields):
        temp_field = 'field'+str(i)
        field_dict[temp_field] = fields[temp_field]

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model | parser
    response = chain.invoke(field_dict)
    output = {"response": response}

    return jsonify(output)

@app.route('/lang_chain_api/llm_call_with_structured_output',methods=['GET','POST'])
def llm_call_with_structured_output_api():

    some_json = request.get_json()
    query = some_json['query']
    output_schema = some_json['output_schema']

    structured_model = model.with_structured_output(output_schema)
    response = structured_model.invoke(query)
    output = {"response": response}

    return jsonify(output)

@app.route('/lang_chain_api/ask_to_vector_db',methods=['GET','POST'])
def ask_to_vector_db_api():

    some_json = request.get_json()
    vector_db = some_json['vector_db']
    search_type = some_json['search_type']
    similar_results = some_json['similar_results']
    query = some_json['query']

    vector_data = FAISS.load_local(vector_db,embeddings,allow_dangerous_deserialization=True)
    retriever = vector_data.as_retriever(search_type=search_type,search_kwargs={"k": similar_results},)
    response = retriever.invoke(query)
    #response = response[0].page_content
    answer = []
    for res in response:
        ans = res.page_content
        src = res.metadata['source']
        answer.append({"answer":ans,"source":src})
    output = {"response": answer}

    return jsonify(output)

@app.route('/lang_chain_api/ask_to_vector_db_rag',methods=['GET','POST'])
def ask_to_vector_db_rag_api():

    some_json = request.get_json()
    vector_db = some_json['vector_db']
    #search_type = some_json['search_type']
    #similar_results = some_json['similar_results']
    query = some_json['query']

    vector_data = FAISS.load_local(vector_db,embeddings,allow_dangerous_deserialization=True)
    #retriever = vector_data.as_retriever(search_type=search_type,search_kwargs={"k": similar_results},)
    retriever = vector_data.as_retriever()
    template = """
        Answer this question using the provided context only.

        {question}

        Context:
        {context}
    """

    prompt = ChatPromptTemplate.from_template(template)
    rag_chain = {"context":retriever,"question":RunnablePassthrough()} | prompt | model
    response = rag_chain.invoke(query)

    output = {"response": response.content}

    return jsonify(output)

@app.route('/lang_chain_api/summarize_web_article',methods=['GET','POST'])
def summarize_web_article_api():

    some_json = request.get_json()
    web_url = some_json['web_url']
    summarize_type = some_json['summarize_type']

    loader = WebBaseLoader(web_url)
    docs = loader.load()

    chain = load_summarize_chain(model, chain_type=summarize_type)
    result = chain.invoke(docs)

    output = {"response": result["output_text"]}

    return jsonify(output)

@app.route('/lang_chain_api/talk_to_database',methods=['GET','POST'])
def talk_to_database_api():

    some_json = request.get_json()
    db_user = some_json['db_user']
    db_password = some_json['db_password']
    db_name = some_json['db_name']
    template = some_json['template']
    query = some_json['query']
    print(query)

    mysql_uri = 'mysql+mysqlconnector://'+db_user+':'+db_password+'@localhost:3306/'+db_name
    db = SQLDatabase.from_uri(mysql_uri)

    prompt_template = ChatPromptTemplate.from_template(template)
    agent_executor = create_sql_agent(model, db=db, agent_type="openai-tools", verbose=True)

    response = agent_executor.run(prompt_template.format_prompt(user_query=query))

    output = {"response": response}

    return jsonify(output)

@app.route('/lang_chain_api/classification_llm_call',methods=['GET','POST'])
def classification_llm_call_api():

    some_json = request.get_json()
    query = some_json['query']

    tagging_llm = model.with_structured_output(Classification)
    tagging_chain = tagging_prompt | tagging_llm

    res = tagging_chain.invoke({"input": query})
    sentiment = res.sentiment
    aggressiveness = res.aggressiveness
    language = res.language

    output = {"response": {"sentiment":sentiment,"aggressiveness":aggressiveness,"language":language}}

    return jsonify(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80,debug=True)