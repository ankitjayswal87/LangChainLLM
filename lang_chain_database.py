import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["MISTRAL_API_KEY"] = os.getenv('MISTRAL_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

mysql_uri = 'mysql+mysqlconnector://langchain:8FRf4T@localhost:3306/online_order'

db = SQLDatabase.from_uri(mysql_uri)
#data = db.run("SELECT * FROM ast_sippeers;")
#print(data)

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many customers are there in database"})
print(response)
data = db.run(response)
print(data)