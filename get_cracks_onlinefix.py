import requests
from bs4 import BeautifulSoup
from cookies import cookies

cookies = cookies

headers = {
    'authority': 'online-fix.me',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en,en-US;q=0.9,fr;q=0.8',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'referer': 'https://online-fix.me/index.php?do=search&subaction=search&story=It+Takes+Two',
    'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"117.0.5938.157"',
    'sec-ch-ua-full-version-list': '"Chromium";v="117.0.5938.157", "Not;A=Brand";v="8.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
}

def search_online(motif:str):
    response = requests.get(f'https://online-fix.me/index.php?do=search&subaction=search&story={motif.replace(" ","+")}', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')
    results = soup.find_all('div',class_='article-content')
    names_list = []
    torrent_url_list = []
    for r in results:
        if (r.find_all('a')[1].h2):
            #needs more filtering more ads/unwanted suggestion appear
            if (motif not in r.find_all('a')[1].h2.text.strip()):
                continue
            
        game_title = r.find_all('a')[2].h2.text.replace("по сети","").strip()
        url = r.find_all('a')[2]['href']
        torrent_link = get_torrent_link(url)
        torrent_url_list.append(torrent_link)
        names_list.append(game_title)
    return list(zip(names_list, torrent_url_list))

def get_torrent_link(url:str):
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text,'html.parser')
    big_div = soup.find('div', class_="quote")
    links = big_div.find_all('a')
    return links[::-1][0]['href']
    