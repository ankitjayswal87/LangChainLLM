import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

# Load the document, split it into chunks, embed each chunk and load it into the vector store.
#raw_documents = TextLoader('openai_test_data.txt').load()

# Load text splitter
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=20,length_function=len,is_separator_regex=False,)
# documents = text_splitter.split_documents(raw_documents)

embeddings = OpenAIEmbeddings()

# SAVE VECTOR DATA TO LOCAL DISK - ONE TIME
# vector_data = FAISS.from_documents(documents, embeddings)
# file_path = "openai_vector_data"
# vector_data.save_local(file_path)

# LOAD VECTOR DATA FROM SAVED DATA ON DISK
vector_data = FAISS.load_local("openai_vector_data",embeddings,allow_dangerous_deserialization=True)
retriever = vector_data.as_retriever(search_type="similarity",search_kwargs={"k": 2},)
query = "what is CPaaS solution"
docs = vector_data.similarity_search(query)
#print(docs[0].page_content)

data = retriever.batch(["what is CPaaS solution", "who is ankit jayswal"])
#print(data[0][0].page_content)
#print(data[0][0].metadata)

#print(data[1][0].page_content)
#print(data[1][0].metadata)
data = retriever.invoke("what is CPaaS solution")
for dt in data:
    print(dt.page_content)
    print("#######################################################")
