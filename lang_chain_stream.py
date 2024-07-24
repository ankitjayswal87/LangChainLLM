import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

system_template = "I love {game}" #"Translate the following into {language}:"
user_template = "let me know highest score of {player}"

prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', user_template)
])

model = ChatOpenAI(temperature=0.6)
parser = StrOutputParser()

chain = prompt_template | model | parser

#data = chain.invoke({"game": "cricket", "player": "Virendra Sehwag"})

#call sync function to render answer
for chunk in chain.stream({"game": "cricket", "player": "Virendra Sehwag"}):
    print(chunk, end="|", flush=True)

#async function and call it to render answer
# async def print_data():
#     async for chunk in chain.astream({"game": "cricket", "player": "Virendra Sehwag"}):
#         print(chunk, end="|", flush=True)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(print_data())
# loop.close()