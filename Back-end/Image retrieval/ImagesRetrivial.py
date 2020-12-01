import os
import numpy as np
from ImageFeatures import getImageFeatures, getDistances
from sklearn.preprocessing import MinMaxScaler

from pandas import DataFrame

NUM_BIN = 16

PATH = "D:/CS Courses/CS 576/Project/Data_jpg/ads/ads_1"
# PATH = "./data"

filename = os.listdir(PATH)
if os.path.exists("data_feature.npy"):
    data_feature = np.load("data_feature.npy")
    data_hist = np.load("data_hist.npy")
else:
    n = len(filename)
    data_feature = np.zeros([n, 17])
    data_hist = np.zeros([n, NUM_BIN ** 3])
    for i in range(n):
        data_hist[i], data_feature[i] = getImageFeatures(PATH + "/" + filename[i])
        
    np.save("data_feature", data_feature)
    np.save("data_hist", data_hist)


query_hist, query_feature = getImageFeatures("2.jpg");

minv = float("inf")
ret = 0
for i in range(len(data_feature)):
    d = getDistances((query_hist, query_feature), (data_hist[i], data_feature[i]))
    if (d < minv):
        minv = d
        ret = i
        
    
print(filename[ret])

