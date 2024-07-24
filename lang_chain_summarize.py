import os
from dotenv import load_dotenv
load_dotenv()
from bs4 import BeautifulSoup

from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["MISTRAL_API_KEY"] = os.getenv('MISTRAL_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

loader = WebBaseLoader("https://telephonyhub.in/2023/01/13/how-to-make-auto-dialer-with-asterisk/")
docs = loader.load()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
chain = load_summarize_chain(llm, chain_type="stuff")

result = chain.invoke(docs)

print(result["output_text"])