
'''
    This web scraper is only used for educational purposes
'''

import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd 
import json
import re
import pickle

print("getting urls...")

urls_file = open("urls.txt", "rb")
urls = pickle.load(urls_file)
urls_file.close


'''

urls = [
    "https://www.yelp.com/biz/guzman-y-gomez-singapore-5",
    "https://www.yelp.com/biz/soup-nutsy-toronto?page_src=related_bizes",
    "https://www.yelp.com/biz/chilis-niagara-falls-2?osq=Chillis",
    "https://www.yelp.com/biz/hoshino-coffee-singapore?page_src=related_bizes",
    "https://www.yelp.com/biz/jimmy-monkey-cafe-and-bar-singapore?page_src=related_bizes", 
    "https://www.yelp.com/biz/the-beast-singapore",
    "https://www.yelp.com/biz/loof-singapore",
    "https://www.yelp.com/biz/working-title-singapore-2",
    "https://www.yelp.com/biz/jumbo-seafood-singapore-4",
    "https://www.yelp.com/biz/tian-tian-hainanese-chicken-rice-singapore-7",
    "https://www.yelp.com/biz/song-fa-bak-kut-teh-singapore-11",
    "https://www.yelp.com/biz/liao-fan-hawker-chan-singapore-3",
    "https://www.yelp.com/biz/din-tai-fung-singapore-5",
    "https://www.yelp.com/biz/swee-choon-tim-sum-singapore",
    "https://www.yelp.com/biz/salt-grill-and-sky-bar-singapore",
    "https://www.yelp.com/biz/the-naked-finn-singapore",
    "https://www.yelp.com/biz/zhong-guo-la-mian-xiao-long-bao-singapore",
    "https://www.yelp.com/biz/tim-ho-wan-singapore-7",
    "https://www.yelp.com/biz/edge-singapore",
    "https://www.yelp.com/biz/vatos-urban-tacos-singapore",
    "https://www.yelp.com/biz/mtr-1924-singapore-2",
    "https://www.yelp.com/biz/cut-singapore-2",
    "https://www.yelp.com/biz/waku-ghin-singapore",
    "https://www.yelp.com/biz/spago-by-wolfgang-puck-singapore", 
    "https://www.yelp.com/biz/hokkaido-ramen-santouka-singapore"

    ]
'''

reviews = pd. DataFrame(columns=['restaurant_name', 'content', 'stars', 'date'])

file_delete = open('reviews.json', 'w') 
file_delete.close()

for url in urls: 
    print("scrapping: https://www.yelp.com"+url+"...")
    request = urllib.request.Request("https://www.yelp.com"+url)
    response = urllib.request.urlopen(request)
    html = response.read().decode('unicode_escape')
    soup = BeautifulSoup(html, "html.parser")
    type(soup)

    reviews_content = []
    reviews_stars = []
    reviews_date_string = []
    reviews_date_datetime = []

    restaurant_name_h1 = soup.find(name="h1", attrs={"class":["lemon--h1__373c0__2ZHSL"]})
    if(restaurant_name_h1 is None):
        continue
    restaurant_name = restaurant_name_h1.getText()

    for div in soup.find_all(name="p", attrs={"class":["comment__373c0__3EKjH"]}):
        review = div.find(name="span", attrs={"class": ["lemon--span__373c0__3997G"]})
        reviews_content.append(review.getText())

    for div in soup.find_all(name="div", attrs={"class":["i-stars__373c0__3UQrn"]}):
        reviews_stars.append(div["aria-label"])

    for div in soup.find_all(name="span", attrs={"class":["lemon--span__373c0__3997G"]}):
        if(len(div.getText()) > 2):
            if(div.getText()[2] == '/' or div.getText()[1] == '/'):
                reviews_date_string.append(div.getText())
                reviews_date_datetime.append(datetime.strptime(div.getText(), '%m/%d/%Y'))

    i = 0
    while i < len(reviews_content):
        dictionary = dict()
        dictionary["restaurant_name"] = restaurant_name
        dictionary["content"] = reviews_content[i]
        if(i+1 < len(reviews_stars)):
            dictionary["stars"] = int(re.sub("[^0-9]", "", reviews_stars[i+1]))
        dictionary["date"] = reviews_date_datetime[i].isoformat()
        reviews = reviews.append(dictionary, ignore_index=True)
        i += 1
    
reviews.to_json(r'D:/Data_Mining/Project/reviews.json')