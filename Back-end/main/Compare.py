import os
from glob import glob
from segmentation import Segmentation
import numpy as np
from ImageFeatures import getImageFeatures, getFrameDistances, FrameFeature, getVideoDistances
import pickle
import sys
import cv2
from ImageFeatures import getVideoDistances
def compareTwoVideos(query,label,root):
    pkl_file1 = open(query, 'rb')
    data1 = pickle.load(pkl_file1)
    # dataPath = '/Users/shaoyaqi/Downloads/576/project/output/'+Label 
    database = glob(root+"/*.pkl")
    dis = {}
    for result in database:
        pkl_file2 = open(result, 'rb')
        data2 = pickle.load(pkl_file2)
        d = getVideoDistances(data1["feature"],data2["feature"],min(len(data1["frameList"]),len(data2["frameList"])))
        name = result.split("/")[-1]
        name = name.split(".")[0]
        dis[name] = d
    return dis
# query = '/Users/shaoyaqi/Downloads/576/project/output/query_interview_0.pkl'
# Label = 'interview'
# dis = compareTwoVideos(query,Label)
# print(dis)