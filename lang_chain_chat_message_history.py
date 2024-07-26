import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
        print(type(store[session_id]))
    return store[session_id]


llm = ChatOpenAI()
with_message_history = RunnableWithMessageHistory(llm, get_session_history)
config = {'configurable': {'session_id': 'abc1'}}
response = with_message_history.invoke([HumanMessage(content="Hello, I am Ankit Jayswal, a tech blogger at https://telephonyhub.in/category/large-language-model/")],config=config,)
print(response.content)
response1 = with_message_history.invoke([HumanMessage(content="which blog Ankit Jayswal writes")],config=config,)
print(response1.content)