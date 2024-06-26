import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')


model = ChatOpenAI(model="gpt-3.5-turbo-0125")

json_schema = {
    "title": "Sports",
    "description": "Get highest score of player",
    "type": "object",
    "properties": {
        "game": {
            "type": "string",
            "description": "The sport in sentence",
        },
        "player": {
            "type": "string",
            "description": "The player in the sport",
        },
        "score": {
            "type": "integer",
            "description": "How many runs scored by player",
        },
    },
    "required": ["game", "player","score"],
}
structured_model = model.with_structured_output(json_schema)

data = structured_model.invoke("let me know the highest runs of Sachin Tendulkar in cricket in ODI")

print(data['game'])
print(data['player'])
print(data['score'])
