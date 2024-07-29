import os
from dotenv import load_dotenv
load_dotenv()

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

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
model = ChatOpenAI()
parser = StrOutputParser()

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80,debug=True)