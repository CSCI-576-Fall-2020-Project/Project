import os
import numpy as np

from ImageFeatures import getImageFeatures
from sklearn.preprocessing import MinMaxScaler

from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances
from pandas import DataFrame


PATH = "D:/CS Courses/CS 576/Project/Data_jpg/ads/ads_1"
# PATH = "./data"

filename = os.listdir(PATH)
if os.path.exists("data.npy"):
    data = np.load("data.npy")
else:
    n = len(filename)
    data = np.zeros([n, 17])
    for i in range(n):
        data[i] = getImageFeatures(PATH + "/" + filename[i])
        
    # trans = MinMaxScaler()
    # data = trans.fit_transform(data)
    np.save("data", data)


vector_in = getImageFeatures("2.jpg");

minv = float("inf")
ret = 0
for i in range(len(data)):
    tmp = euclidean_distances(vector_in.reshape(1,-1), data[i].reshape(1,-1))
    if (tmp < minv):
        minv = tmp
        ret = i
        
    
print(filename[ret])

    
dataset = DataFrame(data)
print(dataset.describe())