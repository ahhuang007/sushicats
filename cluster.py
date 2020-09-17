# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 13:51:26 2020

@author: MSI
"""

import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
from multiprocessing import Pool
#from imageai.Detection import ObjectDetection
import scipy
from scipy import ndimage
import time


#%%
#Resizing
def resize(image, shape):    
    n_c_img = cv2.resize(image, (shape[1], shape[0]), interpolation = cv2.INTER_AREA)
    return n_c_img

#%%
def get_num_color(image):
    modified_image = image.reshape(image.shape[0]*image.shape[1], 3)
    i = 1
    clf = KMeans(n_clusters = 1)
    labels = clf.fit(modified_image)
    start = labels.inertia_
    diff = start
    while diff > 0.2 * start:
        i += 1
        clf = KMeans(n_clusters = i)
        labels = clf.fit(modified_image)
        diff = labels.inertia_
    
    num = i
    
    labels = clf.predict(modified_image)
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    
    return num, list(counts.values()), rgb_colors

def get_dom_color(counts, rgbs):
    main_colors = ["Black", "White", "Red", "Green", "Blue", "Yellow", "Cyan", 
                   "Magenta", "Orange", "Lime", "Spring", "Sky", 
                   "Indigo", "Pink", "Maroon", "Olive", "Teal", "Navy"]
    codes = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255),
             (255, 255, 0), (0, 255, 255), (255, 0, 255),
             (255, 128, 0), (128, 255, 0), (0, 255, 128), (0, 128, 255),
             (128, 0, 255), (255, 0, 128), (128, 0, 0), (128, 128, 0),
             (0, 128, 128), (0, 0, 128)]
    scores = [0] * len(main_colors)
    for i in range(len(rgbs)):
        r = rgbs[i][0]
        g = rgbs[i][1]
        b = rgbs[i][2]
        dists = []
        for tup in codes:
            dis = np.sqrt((tup[0]-r)**2 + (tup[1]-g)**2 + (tup[2]-b)**2)
            dists.append(dis)
        mini = dists.index(min(dists))
        scores[mini] += counts[i]
    maxi = scores.index(max(scores))
    
    return main_colors[maxi]

def warmcool(image):
    
    modified_image = image.reshape(image.shape[0]*image.shape[1], 3)
    clf = KMeans(n_clusters = 10)
    labels = clf.fit(modified_image)
    labels = clf.predict(modified_image)
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    counts = list(counts.values())
    color_wheel = ["Red", "Redorange", "Orange", "Yelloworange", "Yellow",
                   "Yellowgreen", "Green", "Bluegreen", "Blue", "Blueviolet",
                   "Violet", "Redviolet", "White", "Black", "Gray"]
    color_codes = [(255, 0, 0), (255, 83, 73), (255, 165, 0), (255, 174, 66),
                   (255, 255, 0), (154, 205, 50), (0, 255, 0), (13, 152, 186),
                   (0, 0, 255), (138, 43, 226), (148, 0, 211), (199, 21, 133),
                   (255, 255, 255), (0, 0, 0), (128, 128, 128)]
    warm = 0
    cool = 0
    bw = 0
    for i in range(len(rgb_colors)):
        r = rgb_colors[i][0]
        g = rgb_colors[i][1]
        b = rgb_colors[i][2]
        dists = []
        for tup in color_codes:
            dis = np.sqrt((tup[0]-r)**2 + (tup[1]-g)**2 + (tup[2]-b)**2)
            dists.append(dis)
        mini = dists.index(min(dists))
        if mini < 6:
            warm += counts[i]
        elif mini > 11:
            bw += counts[i]
        else:
            cool += counts[i]
    if warm > 1.5 * cool and warm > bw:
        return 0
    elif cool > 1.5 * warm and cool > bw:
        return 1
    elif bw / (cool + warm + 1) > 10:
        return 2
    else:
        return 3
    
def get_complexity(image):
    #I mean,I guess number of contours does correlate I think with "complexity"
    ret, thresh = cv2.threshold(image,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU,image)
    #ret,thresh = cv2.threshold(image,127,255,0)
    #image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    image, contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 0.25:
            count += 1     
    return count

def corners(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.2)
    print(len(dst))
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)
    
    # Threshold for an optimal value, it may vary depending on the image.
    image[dst>0.01*dst.max()]=[0,0,255]
    dst = dst[dst>0.01*dst.max()]
    print(len(dst))
    cv2.imshow('dst',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 5

def brightness(image):
    image2 = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return np.mean(image2)

def sharpness(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()
    
#%%
def main_func(df):
    #df = pd.read_csv("C:/Users/MSI/Documents/Github/capstone/Data/big_art_data.csv")
    #df = df.drop([df.columns[0]], axis = 1)
    is_blackandwhite = []
    num_colors = []
    dom_colors = []
    warm_or_cool = [] #0 = warm, 1 = cool, 2 = black/white, 3 = mixture
    complexity = []
    num_corners = []
    brights = []
    sharps = []
    #Testing for now - change to len(df) later
    n = 0
    for i in df:
        #image = cv2.imread(df.loc[i]["Filename"])
        print(i)
        image = cv2.imread(i)
        dims = image.shape
        #preprocessing
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray2 = 255*(gray < 225).astype(np.uint8)
        coords = cv2.findNonZero(gray2) # Find all non-zero points (text)
        x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
        if x == 0 and y == 0 and w == 0 and h == 0:
            gray2 = 255*(gray < 245).astype(np.uint8)
            coords = cv2.findNonZero(gray2) # Find all non-zero points (text)
            x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
        image = image[y:y+h, x:x+w] # Crop the image - note we do this on the original image
        gray = gray[y:y+h, x:x+w]
        try:
            image = resize(image, dims)
            gray = resize(gray, dims)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
            num, counts, rgbs = get_num_color(image)
            num_colors.append(num)
            color = get_dom_color(counts, rgbs)
            dom_colors.append(color)
            wcb = warmcool(image)
            warm_or_cool.append(wcb)
            comp = get_complexity(gray)
            complexity.append(comp)
            #co = corners(image)
            #num_corners.append(co)
            br = brightness(image)
            brights.append(br)
            sh = sharpness(gray)
            sharps.append(sh)
        except:
            print("fuck this stupid image")
            num_colors.append("null")
            dom_colors.append("null")
            warm_or_cool.append("null")
            complexity.append("null")
            brights.append("null")
            sharps.append("null")
        
        #plt.imshow(image)
    '''
    df["num_colors"] = num_colors
    df["dom_color"] = dom_colors
    df["warm_cool"] = warm_or_cool
    df["complexity"] = complexity
    df["brightness"] = brights
    df["sharpness"] = sharps
    '''
    return [num_colors, dom_colors, warm_or_cool, complexity, brights, sharps]
    #%%

    #df.to_csv("C:/Users/MSI/Documents/Github/capstone/Data/processed_data.csv")
if __name__ == "__main__":
    df = pd.read_csv("C:/Users/MSI/Documents/Github/capstone/Data/big_art_data.csv")
    #df = pd.read_csv("big_art_data.csv")
    df = df[189000:]    
    df = df.drop([df.columns[0]], axis = 1)
    dfi = list(df["Filename"])
    
    group1 = dfi[0:2378]
    group2 = dfi[2378:4756]
    group3 = dfi[4756:7134]
    group4 = dfi[7134:9512]
    group5 = dfi[9512:11890]
    group6 = dfi[11890:14268]
    group7 = dfi[14268:]
    
    start = time.time()
    
    with Pool(processes = 7) as pool:
        print("processes")
        list1 = pool.apply_async(main_func, ([group1]))
        list2 = pool.apply_async(main_func, ([group2]))
        list3 = pool.apply_async(main_func, ([group3]))
        list4 = pool.apply_async(main_func, ([group4]))
        list5 = pool.apply_async(main_func, ([group5]))
        list6 = pool.apply_async(main_func, ([group6]))
        list7 = pool.apply_async(main_func, ([group7]))
        #list8 = pool.apply_async(main_func, ([group8]))
        #list9 = pool.apply_async(main_func, ([group9]))
        #list0 = pool.apply_async(main_func, ([group0]))
        print("getting")
        list1 = list1.get()
        list2 = list2.get()
        list3 = list3.get()
        list4 = list4.get()
        list5 = list5.get()
        list6 = list6.get()
        list7 = list7.get()
        #list8 = list8.get()
        #list9 = list9.get()
        #list0 = list0.get()
    
    end = time.time()
    print("Time consumed in working: ",end - start)
    nc = list1[0] + list2[0] + list3[0] + list4[0] + list5[0] + list6[0] + list7[0] #list9[0] + list0[0] + lastdf[0]
    dc = list1[1] + list2[1] + list3[1] + list4[1] + list5[1] + list6[1] + list7[1] #list9[1] + list0[1] + lastdf[1]
    wc = list1[2] + list2[2] + list3[2] + list4[2] + list5[2] + list6[2] + list7[2] #list9[2] + list0[2] + lastdf[2]
    co = list1[3] + list2[3] + list3[3] + list4[3] + list5[3] + list6[3] + list7[3] #list9[3] + list0[3] + lastdf[3]
    br = list1[4] + list2[4] + list3[4] + list4[4] + list5[4] + list6[4] + list7[4] #list9[4] + list0[4] + lastdf[4]
    sh = list1[5] + list2[5] + list3[5] + list4[5] + list5[5] + list6[5] + list7[5] #list9[5] + list0[5] + lastdf[5]
    df["num_colors"] = nc
    df["dom_color"] = dc
    df["warm_cool"] = wc
    df["complexity"] = co
    df["brightness"] = br
    df["sharpness"] = sh
    print(df)
    
    df.to_csv("C:/Users/MSI/Documents/Github/capstone/Data/big_processed_data_p11.csv")
    #df.to_csv("big_processed_data.csv")
    
    
