import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

embeddings = OpenAIEmbeddings()

# LOAD VECTOR DATA FROM SAVED DATA ON DISK
vector_data = FAISS.load_local("openai_vector_data",embeddings,allow_dangerous_deserialization=True)
retriever = vector_data.as_retriever(search_type="similarity",search_kwargs={"k": 1},)

template = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")

rag_chain = {"context":retriever,"question":RunnablePassthrough()} | prompt | llm

response = rag_chain.invoke("what is programmable voice interface")

print(llm.invoke("who  is Ankit Jayswal").content)
print("######################################################")
print(response.content)

# query = "let me know about ankit jayswal" #"what is CPaaS solution"
# docs = vector_data.similarity_search(query)
# print("######################################################")
# print(docs[0].page_content)

# data = retriever.batch(["what is CPaaS solution", "who is ankit jayswal"])
# print(data[0][0].page_content)
# print(data[0][0].metadata)

# print(data[1][0].page_content)
# print(data[1][0].metadata)
