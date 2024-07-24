import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

llm = ChatOpenAI()
memory = ConversationBufferWindowMemory(k=1)

conversation_chain = ConversationChain(llm=llm,memory=memory,verbose=True)

conversation_chain.predict(input="Hello, Ankit is Zalak's brother")
conversation_chain.predict(input="Both are the kids of same parents")
conversation_chain.predict(input="who is Zalak? answer in short")
print(memory.buffer)