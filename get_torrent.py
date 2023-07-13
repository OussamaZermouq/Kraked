import requests
import torrentool
from bs4 import BeautifulSoup
from urllib import parse
import re 
import wget

session  = requests.Session()

#the dumbest code on the planet, yet it works, dont judge me there is no API so we scrapy scrape
def search(motif):
    output = {}
    url_test=f"https://1337x.to/sort-category-search/{motif.replace(' ','-')}/Games/time/desc/1/"
    print(url_test)
    response = session.get(url=url_test)
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


def fetch_hash(name):
    results  = search(name).keys()
    hash=[]
    counter = 0
    for result in results:
        counter+=1
        if name == result:
            url = f'https://1337x.to{result}'
            print(url)
            if counter>1:
                return -2
            r = requests.get(url)
            soup = BeautifulSoup(r.text,'html.parser')
            hash_tag= soup.find('div',class_ = 'infohash-box')
            for tags in hash_tag.children:
                if len(tags)>=2:
                    hash = tags.text.split()
            break
        else:
            continue

    if len(hash)>=2:
        return hash[2]
    else:
        return -1

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


print(grab_torrent(fetch_hash('Forza.horizon.5.PROPER-EMPRESS')))