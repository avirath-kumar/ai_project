import requests

# set paratmeters for API call
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer ",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Write me a haiku about my first ai coding project in python"}],
    "temperature": 0.7
}

# api call happens here
response = requests.post(url, json=data, headers=headers)

# handle api call output
if response.status_code == 200:
    print(response.json()['choices'][0]['message']['content']) # syntax to isolate the 'content' dict
else:
    print(f"Error: {response.json()}") # might need to edit this based on what kind of error gets returned

# DELETE BEARER TOKEN BEFORE PUSHING