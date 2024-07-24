import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')


tagging_prompt = ChatPromptTemplate.from_template(
"""
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""
)

class Classification(BaseModel):
    sentiment: str = Field(description="The sentiment of the text")
    aggressiveness: int = Field(
        description="How aggressive the text is on a scale from 1 to 10"
    )
    language: str = Field(description="The language the text is written in")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125").with_structured_output(
    Classification
)

tagging_chain = tagging_prompt | llm

inp = "Hey you are looking beutiful"
res = tagging_chain.invoke({"input": inp})
print(res)