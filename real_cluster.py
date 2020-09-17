# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 11:27:56 2020

@author: MSI
"""
import pandas as pd
import numpy as np
import gower
from sklearn.neighbors import DistanceMetric
from scipy.sparse import issparse



df = pd.read_csv("C:/Users/ahhua/Documents/Github/capstone/Data/processed_data.csv")
df = df.drop([df.columns[0]], axis = 1)

df = df.drop(['Title','Size','Link','Filename','Src'], axis = 1)
cate = [0]
cate.extend([1]*43)
cate.extend([0,1,0,0,0,0])
weights = [2]+(43*[1]) + (6*[5])
print('q')
g = gower.gower_matrix(df,weight=np.array(weights), cat_features=cate)
print('r')
pred = gower.gower_topn(df.iloc[0:2,:], df.iloc[:,], n = 5, weight=np.array(weights), cat_features=cate)
print(pred)
'''
area = DistanceMetric.get_metric('manhattan').pairwise(df[['Area']])
area = area/max(np.ptp(df['Area']),1)

num_colors = DistanceMetric.get_metric('manhattan').pairwise(df[['num_colors']])
num_colors = num_colors/max(np.ptp(df['num_colors']),1)

complexity = DistanceMetric.get_metric('manhattan').pairwise(df[['complexity']])
complexity = complexity/max(np.ptp(df['complexity']),1)

bright = DistanceMetric.get_metric('manhattan').pairwise(df[['brightness']])
bright = bright/max(np.ptp(df['brightness']),1)

sharp = DistanceMetric.get_metric('manhattan').pairwise(df[['sharpness']])
sharp = sharp/max(np.ptp(df['sharpness']),1)
'''
