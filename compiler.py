# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 14:28:34 2020

@author: ahhua
"""

import pandas as pd
import numpy as np
import random
path = "C:/Users/ahhua/Documents/Github/capstone/Code/Data/"
dfs = []
for i in range(1,12):
    df = pd.read_csv(path + "big_processed_data_p" + str(i) + ".csv")
    dfs.append(df)
    
bigdf = pd.concat(dfs).reset_index(drop = True)
nulls = list(bigdf[bigdf["dom_color"].isnull()].index)
bigdf = bigdf.drop(nulls)

bigdf = bigdf.drop([df.columns[0]], axis = 1).reset_index(drop = True)
partials = []
l = list(range(205643))
for i in range(195000):
    #num = np.random.randint(0,205643)
    num = l.pop(random.randrange(len(l)))
    #while num in partials:
        #num = np.random.randint(0,205643)
    partials.append(num)
partdf = bigdf[bigdf.index.isin(partials)]
partdf.to_csv(path + "p_compiled_data.csv")
'''
subjects = [('Abstract', '1822'), ('Animals', '1823'), ('Architecture', '1824'),
            ('Art-For-Kids', '1846'), ('Astronomy-Space', '1849'), 
            ('Book-Illustration', '16123'), ('Botanical', '12134'), 
            ('Comics', '12105'), ('Conde-Nast-Magazines', '428722'), 
            ('Costume-Fashion', '20122'), ('Cuisine', '1850'), 
            ('Dance', '2847'), ('Education', '12118'), 
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
'''

partials = []
for i in range(80000):
    num = np.random.randint(0,205643)
    while num in partials:
        num = np.random.randint(0,205643)
    partials.append(num)
partdf = bigdf[bigdf.index.isin(partials)]
print(len(partdf))
partdf.to_csv(path + "partial_data.csv")