import requests
from bs4 import BeautifulSoup
import urllib
from urllib import parse
import re 
import json

session  = requests.Session()

#just scraping data from bitsearch.to dont mind if i do

#the dumbest code on the planet, yet it works, dont judge me there is no API so we scrapy scrape
def search(motif):
    output = {}
    url_test=f"https://bitsearch.to/search?q={urllib.parse.quote(motif)}&category=6&subcat=1&sort=date"
    #test subject : https://bitsearch.to/search?q=demonologist&category=6&subcat=1
    response = session.get(url=url_test)
    soup = BeautifulSoup(response.text,'html.parser')
    release_list = soup.find_all('h5',class_='title w-100 truncate')
    print(soup)
    img_size_tags = soup.find_all('img', {'alt': 'Size'})
    download_links = soup.find_all('a',class_='dl-torrent')
    seeders_counts = soup.find_all('img', {'alt': 'Seeder'})

    names_list =[]
    sizes_list =[]
    dl_link_list=[]
    seeders_counts_list=[]
    for img_tag in img_size_tags:
        size_div = img_tag.find_parent('div')
        size = size_div.get_text(strip=True)
        sizes_list.append(size)

    for names in release_list:
        release_names = names.find_all('a', href=True)
        for release_name in release_names:
            names_list.append(release_name.text)
    
    for download_link in download_links:
        dl_link_list.append(download_link.get('href'))

    for seeder_count in seeders_counts:
        seeder_count_div = seeder_count.find_parent('div')
        seeder_count_text = seeder_count_div.get_text(strip=True)
        seeders_counts_list.append(seeder_count_text)

    return list(zip(names_list,sizes_list,seeders_counts_list,dl_link_list))
    
