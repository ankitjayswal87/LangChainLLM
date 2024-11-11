from langchain_community.llms import Ollama

llm = Ollama(model="gemma:2b")

response = llm.invoke("tell me about partial functions in python")
print(response)
