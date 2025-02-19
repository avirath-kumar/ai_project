import requests

url = "https://fakestoreapi.com/products/1"
response = requests.get(url)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")