import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

loader = PyPDFLoader("BuildingChatBotsWithTwilio.pdf")
pages = loader.load_and_split()
#print(pages)

embeddings = OpenAIEmbeddings()

template = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
parser = StrOutputParser()

vector_data = FAISS.from_documents(pages, embeddings)
retriever = vector_data.as_retriever(search_type="similarity",search_kwargs={"k": 1},)

chain = {"context":retriever,"question":RunnablePassthrough()} | prompt | model | parser
response = chain.invoke("benefits of chatbot")
print(response)