# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 21:12:54 2020

@author: MSI
"""

import os
import urllib.request
import requests
import urllib
import pandas as pd
from bs4 import BeautifulSoup
import re
from cluster import main_func

def get_artwork(term, dire, used_links, rows_list, cats):
    #First page
    url = 'https://www.art.com/gallery/id--b' + term[1] + '/' + term[0] + '-posters.htm'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')    
    images = soup.select('img[class ="grid-image"]')
    title = soup.select('a[class = "product-title"]')
    size = soup.select('div[class = "size-container"]')
    num = soup.select('span[class = "item-count secondary-text"]')[0].get_text()
    tl = list(num.split())
    totalnum = tl[0]
    totalnum = int(totalnum.replace(',',''))
    pages = int(totalnum // 60 // 1.5)
    img_ct = 0
    pattern = re.compile(r'(\d+)"\sx\s(\d+)"')
    headers2={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                      'Accept-Encoding': 'none',
                      'Accept-Language': 'en-US,en;q=0.8',
                      'Connection': 'keep-alive'}
    for i in range(len(images)):
        el = images[i]
        img_url = el.get("src")
        if img_url not in used_links:
            try:
                request_= urllib.request.Request(img_url,None,headers2) #The assembled request
                response = urllib.request.urlopen(request_)# store the response
                el2 = title[i].get("title")
                el3 = size[i].select('span[class = "size"]')[0].get_text()
                el4 = title[i].get("href")
                m = re.search(pattern, el3)
                newdict = dict.fromkeys(cats, 0)
                newdict["Title"] = el2
                newdict["Size"] = (int(m[1]), int(m[2]))
                newdict["Link"] = el4
                newdict["Area"] = int(m[1]) * int(m[2])
                newdict["Filename"] = dire + term[0] + "_img_" + str(img_ct) + ".jpg"
                newdict["Src"] = img_url
                newdict["is_" + term[0]] = 1
                
                
                #create a new file and write the image
                f = open(dire + term[0] + "_img_" + str(img_ct) + ".jpg",'wb')
                f.write(response.read())
                f.close()
                img_ct += 1
                used_links.append(img_url)
                rows_list.append(newdict)
            except:
                print("error occurred, image probably not there")
        else:
            q = next((i for i, item in enumerate(rows_list) if item["Src"] == img_url), None)
            rows_list[q]["is_" + term[0]] = 1
    #Successive pages
    for i in range(2,pages):
        url = "https://www.art.com/gallery/id--b" + term[1] + "/" + term[0] + "-posters.htm?page=" + str(i) + "&pathNumber=0"
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.text, 'html.parser')    
        images = soup.select('img[class ="grid-image"]')
        title = soup.select('a[class = "product-title"]')
        size = soup.select('div[class = "size-container"]')
        for i in range(len(images)):
            el = images[i]
            img_url = el.get("src")
            if img_url not in used_links:
                try:
                    request_= urllib.request.Request(img_url,None,headers2) #The assembled request
                    response = urllib.request.urlopen(request_)# store the response
                    el2 = title[i].get("title")
                    el3 = size[i].select('span[class = "size"]')[0].get_text()
                    el4 = title[i].get("href")
                    m = re.search(pattern, el3)
                    newdict = dict.fromkeys(cats, 0)
                    newdict["Title"] = el2
                    newdict["Size"] = (int(m[1]), int(m[2]))
                    newdict["Link"] = el4
                    newdict["Area"] = int(m[1]) * int(m[2])
                    newdict["Filename"] = dire + term[0] + "_img_" + str(img_ct) + ".jpg"
                    newdict["Src"] = img_url
                    newdict["is_" + term[0]] = 1
    
                    
                    #create a new file and write the image
                    f = open(dire + term[0] + "_img_" + str(img_ct) + ".jpg",'wb')
                    f.write(response.read())
                    f.close()
                    img_ct += 1
                    used_links.append(img_url)
                    rows_list.append(newdict)
                except:
                    print("error occurred, image probably not there") 
            else:
                q = next((i for i, item in enumerate(rows_list) if item["Src"] == img_url), None)
                rows_list[q]["is_" + term[0]] = 1
    
    return used_links, rows_list
#%%

subjects = [('Abstract', '1822'), ('Animals', '1823'), ('Architecture', '1824'),
            ('Art-For-Kids', '1846'), ('Astronomy-Space', '1849'), 
            ('Book-Illustration', '16123'), ('Botanical', '12134'), 
            ('Comics', '12105'), ('Conde-Nast-Magazines', '428722'), 
            ('Costume-Fashion', '20122'), ('Cuisine', '1850'), 
            ('Dance', '2847'), ('Disney', '24384'), ('Education', '12118'), 
            ('Fantasy', '1843'), ('Figurative' ,'12132'), 
            ('Geodes-And-Minerals', '1895591'), ('Geometrics-Art', '1902553'), 
            ('Hobbies', '25932'), ('Holidays', '7910'), ('Home-Hearth', '7569'), 
            ('Humor', '1853'), ('Japandi', '38921'), ('Maps', '1852'), 
            ('Maximalist-Art', '39168'), ('Motivational', '1945'), ('Movies', '1881'), 
            ('Museums', '274479'), ('Music', '1851'), ('People', '1841'), 
            ('Places', '6473'), ('Religion-Spirituality', '12114'), ('Scenic', '1833'), 
            ('Performing-Arts', '155853'),  ('Publications', '206294'), 
            ('Seasons', '12139'), ('Sports', '1834'), ('Still-Life', '1854'), 
            ('Television', '1882'), ('The-New-Yorker', '428656'),
            ('Transportation', '1836'), ('Typography-Symbols', '228302'), 
            ('World-Culture', '1838')]

cats = ["Title", "Size", "Area", "Link", "Filename", "Src"]
for el in subjects:
    cats.append("is_" + el[0])
os.makedirs("C:/query_data/art_images", exist_ok = True)
img_dir = "C:/query_data/art_images/"
used_links = []
rows_list = []
for term in subjects:
    print(term[0])
    os.makedirs("C:/query_data/art_images/" + term[0], exist_ok = True)    
    dire = "C:/query_data/art_images/" + term[0] + "/"
    used_links, rows_list = get_artwork(term, dire, used_links, rows_list, cats)
    
big_bad_df = pd.DataFrame(rows_list, columns = cats)
big_bad_df.to_csv("C:/Users/ahhua/Documents/Github/capstone/Code/Data/big_art_data.csv")

main_func()
