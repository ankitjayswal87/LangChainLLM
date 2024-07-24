import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import chain

prompt1 = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
prompt2 = ChatPromptTemplate.from_template("What is the subject of this joke: {joke}")


@chain
def custom_chain(text):
    prompt_val1 = prompt1.invoke({"topic": text})
    #print(prompt_val1)
    output1 = ChatOpenAI().invoke(prompt_val1)
    parsed_output1 = StrOutputParser().invoke(output1)
    print(parsed_output1)
    chain2 = prompt2 | ChatOpenAI() | StrOutputParser()
    return chain2.invoke({"joke": parsed_output1})


data = custom_chain.invoke("bears")
#print(data)