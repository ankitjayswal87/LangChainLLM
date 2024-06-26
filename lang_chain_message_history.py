import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory


def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

prompt_template = ChatPromptTemplate.from_template("Hey, I am Ankit Jayswal")

model = ChatOpenAI(temperature=0.6)
parser = StrOutputParser()

chain = prompt_template | model | parser

runnable_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
)

runnable_with_history.invoke(chain,config={'configurable': {'session_id': 'abc123'}})