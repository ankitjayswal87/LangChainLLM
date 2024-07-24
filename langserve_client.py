import requests

response = requests.post(
    "http://localhost:8000/joke/invoke",
    json={'input': {'person': 'ankit jayswal'}}
)
print(response.json()['output']['content'])
