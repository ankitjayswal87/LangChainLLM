import os
from dotenv import load_dotenv
load_dotenv()

#from langchain.llms import OpenAI
#from langchain_community.llms import OpenAI
#from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
#from langchain.prompts import PromptTemplate
#from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')



#llm = OpenAI(temperature=0.6)
#name = llm.invoke("I want to open a restaurant for Indian food. suggest fency name for this.")
#name = llm.invoke("I want to open a telecom business, please suggest name for that.")

#prompt_template_name = PromptTemplate(input_variables = ['cuisine'],template="I want to open a restaurant for {cuisine} food. suggest fency name for this.")
#format_data = prompt_template_name.format(cuisine="Italian")
#print(format_data)

system_template = "I love {game}" #"Translate the following into {language}:"
user_template = "let me know highest score of {player}"

prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', user_template)
])

model = ChatOpenAI(temperature=0.6)
parser = StrOutputParser()

chain = prompt_template | model | parser

data = chain.invoke({"game": "cricket", "player": "Virendra Sehwag"})
print(data)
