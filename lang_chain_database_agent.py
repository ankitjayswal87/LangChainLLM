import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.agent_toolkits import create_sql_agent

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["MISTRAL_API_KEY"] = os.getenv('MISTRAL_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

# database connection
mysql_uri = 'mysql+mysqlconnector://admin:LenArWXwm3fcVSfX@localhost:3306/store'
db = SQLDatabase.from_uri(mysql_uri)

# prompt template to give description about database and database tables
template = """You are an expert AI assistant who answers user queries from looking into the mysql database called store.
The store database has following tables:
company_employee,t_shirts
The company_employee table has following fields:
first_name,last_name,age
The t_shirts table has following fields:
colour,size,type
Please answer for below user_query:
{user_query}
"""
prompt_template = ChatPromptTemplate.from_template(template)

# OpenAI LLM object
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# creating sql agent to serve user queries
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

user_query = "who is youngest employee in company"
user_query = "how many white t shirts are availbale in the store of size medium and of round neck type"
response = agent_executor.run(prompt_template.format_prompt(user_query=user_query))
print("#################### ANSWER #########################")
print("ANSWER: "+response)

# response = agent_executor.invoke(
#     {
#         "input": "how many black t shirts are availbale in the store of size medium and v neck type"
#     }
# )
# print(response['output'])