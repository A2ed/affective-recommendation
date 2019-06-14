"""
This script scrapes a scotch website for product descriptions and user reviews.
All the data is currently saved in reviews_v3.csv
"""

import requests
from bs4 import BeautifulSoup
import re

### generate dictionary of scotch types and urls
for n in range(1,105):
    # get website data
    page = requests.get(f'https://www.masterofmalt.com/country-style/scotch/single-malt-whisky/{n}')
    # parse html
    soup = BeautifulSoup(page.content, 'html.parser')
    # extract info from product boxes
    scotch_list = soup.find_all('div', attrs={'class' : 'boxBgr product-box-wide h-gutter js-product-box-wide'})
    # loop through individual products
    for scotch in scotch_list:
        # filter discontinued
        if scotch.find('div', attrs={'class' : 'mom-btn-text'}).text != 'Discontinued':
            # add scotch name and product url to review dictionary
            reviews[scotch.attrs['data-name']] = {'url' : scotch.attrs['data-product-url']}

# scrape data from product urls
for k,v in reviews.items():
    # get website data
    page = requests.get(v['url'])
    # parse html
    soup = BeautifulSoup(page.content, 'html.parser')
    # extract description
    v['description'] = soup.find('div', attrs={'itemprop' : 'description'}).get_text(strip=True)
    # extract price
    v['price'] = soup.find('div', class_='priceDiv').get_text(strip=True)
    # code sold out status
    if soup.find('div', attrs={'class' : 'mom-btn-text'}).text == 'Sold out':
        v['sold_out'] = 1
    else:
        v['sold_out'] = 0
    # extract rating
    try:
        v['rating'] = soup.find('meta', attrs={'itemprop' : 'ratingValue'}).extract
    except:
        pass
    # extract palate information
    try:
        v['nose'] = soup.find('p', attrs={'id' : 'ContentPlaceHolder1_ctl00_ctl02_TastingNoteBox_ctl00_noseTastingNote'}).get_text(strip=True)
    except:
        pass
    try:
        v['palate'] = soup.find('p', attrs={'id' : 'ContentPlaceHolder1_ctl00_ctl02_TastingNoteBox_ctl00_palateTastingNote'}).get_text(strip=True)
    except:
        pass
    try:
        v['finish'] = soup.find('p', attrs={'id' : 'ContentPlaceHolder1_ctl00_ctl02_TastingNoteBox_ctl00_finishTastingNote'}).get_text(strip=True)
    except:
        pass
    try:
        v['overall'] = soup.find('p', attrs={'id' : 'ContentPlaceHolder1_ctl00_ctl02_TastingNoteBox_ctl00_overallTastingNote'}).get_text(strip=True)
    except:
        pass
    # review list
    review_list = []
    # loop through reviews
    for i in soup.find_all('p', attrs={'itemprop' : 'reviewBody'}):
        review_list.append(i.text)
    # add reviews to dictionary
    v['reviews'] = review_list
