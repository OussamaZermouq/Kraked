import requests



search_query = 'f1.2020'
url =f'https://api.srrdb.com/v1/search/{search_query}/category:pc'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for releases in data["results"]:
        print(releases["release"])
else:
    print(f'Error {response.status_code}')