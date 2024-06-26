import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

model = ChatOpenAI()
joke_chain = ChatPromptTemplate.from_template("tell me a joke about {topic}") | model
poem_chain = ChatPromptTemplate.from_template("write a 2-line poem about {topic}") | model

map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

data = map_chain.invoke({"topic": "bear"})
print(data['joke'].content)
print(data['poem'].content)