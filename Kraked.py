import requests


url ='https://api.predb.net/?q=spiderman&genre=GAMES'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data["data"]["release"])
else:
    print(f'Error {response.status_code}')