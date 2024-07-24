import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')


@tool
def add(a: int, b: int):
    """Adds a and b."""
    return a+b

@tool
def multiply(a: int, b: int):
    """Multiplies a and b."""
    return a*b

tools = [add, multiply]

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
llm_with_tools = llm.bind_tools(tools)
tool_call_data = llm_with_tools.invoke("what is 3 * 5 and what is 4 +48?").tool_calls #[{'name': 'add', 'args': {'a': 3, 'b': 5}, 'id': 'call_jitDoFeSgE6ICNQpgIelPGO1'}]

data_messages = []
for tool_call in tool_call_data:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_output = selected_tool.invoke(tool_call["args"])
    tool_call_id=tool_call["id"]
    tool_call_name=tool_call["name"]
    #data_messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"], tool_call_name=tool_call["name"]))
    print(tool_output)
    print(tool_call_id)
    print(tool_call_name)