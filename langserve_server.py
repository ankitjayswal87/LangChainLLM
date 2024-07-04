import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
import uvicorn

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

app = FastAPI(title="LangChain Server",version="1.0",description="API server to serve REST api calls")

prompt = ChatPromptTemplate.from_template("let me know two lines about {person}")
model = ChatOpenAI(model="gpt-3.5-turbo-0125")

add_routes(app,prompt | model,path="/joke")

uvicorn.run(app,host="localhost",port=8000)