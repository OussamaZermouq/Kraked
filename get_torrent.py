import requests
from bs4 import BeautifulSoup
import urllib
from urllib import parse
import re 

session  = requests.Session()

headers = {
    'User-Agent': 'your_user_agent_here',
    'Accept-Language': 'your_accept_language_here',
    'Referer': 'your_referer_url_here',
}

cookies = {
    'cookie_name': 'cookie_value',
}

#the dumbest code on the planet, yet it works, dont judge me there is no API so we scrapy scrape
def search(motif):
    output = {}
    url_test=f"https://1337x.to/sort-category-search/{urllib.parse.quote(motif)}/Games/time/desc/1/"
    #https://1337x.to/category-search/spider%20man/Games/1/
    response = session.get(url=url_test, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text,'html.parser')
    names = soup.find_all('td',class_='coll-1 name')
    sizes = soup.find_all('td',class_="coll-4 size mob-uploader")
    for name,size in zip(names,sizes):
        links = name.find_all('a', href=True)
        if len(links) >= 2 and links[0]['href']=='/sub/10/0/':
            #print(links[1]['href'])
            size_release = ''.join(size.find_all(string=True, recursive=False)).strip()
            output[links[1]['href']] = size_release
    return output


def fetch_url(key):
    url = f"https://1337x.to{key}"
    response = session.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    hash_div = soup.find('div',class_='infohash-box')
    hash = hash_div.find('span')
    url_torrent = f'http://btcache.me/torrent/{hash.text}'
    return url_torrent

#hash test
#hash='0FA471B97F5F461A1FE58A6220703CC3CFD1C816'
def grab_torrent(hash):
    if hash == -1:
        print('Error recheck your hash')
        exit(-1)
    elif hash == -2:
        print('Too many results try to make your search for')
    url=f'http://itorrents.org/torrent/{hash}.torrent'
    return url


def clean_links(link):
    pattern = r'/([^/]+)/$'
    match = re.search(pattern, link)
    if match:
        extracted_string = match.group(1)
        return extracted_string
