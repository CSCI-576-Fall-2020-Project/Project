import os
from glob import glob
from segmentation import Segmentation
import numpy as np
from ImageFeatures import getImageFeatures, getFrameDistances, FrameFeature, getVideoDistances,getNearstDistances
import pickle
import sys
import cv2
from ImageFeatures import getVideoDistances,getDatabaseScore
class SearchResult:
    def __init__(self):
        self.videoName = ""
        self.totalScore = 0
        self.keyFrames = {}
    def getValue(self,Name,Score,d):
        self.videoName = Name
        self.keyFrames = Score
        self.totalScore = d
def compareTwoVideos(query,label,root):
    pkl_file1 = open(query, 'rb')
    data1 = pickle.load(pkl_file1)
    # dataPath = '/Users/shaoyaqi/Downloads/576/project/output/'+Label 
    database = glob(root+"/*.pkl")
    dis = {}
    results_list=[]
    for result in database:
        pkl_file2 = open(result, 'rb')
        data2 = pickle.load(pkl_file2)
        # d = getVideoDistances(data1["feature"],data2["feature"],min(len(data1["frameList"]),len(data2["frameList"])))
        
        d_foreground = getNearstDistances(data1["feature"][0],data2["feature"][0],len(data1["frameList"]),len(data2["frameList"]))
        d_fullimage = getNearstDistances(data1["feature"][1],data2["feature"][1],len(data1["frameList"]),len(data2["frameList"]))
        
        if d_foreground < d_fullimage:
            d = d_foreground
            keyFrameScore = getDatabaseScore(data1["feature"][0], data2["feature"][0], data2["frameList"], len(data1["frameList"]),len(data2["frameList"]))
        else: 
            d = d_fullimage
            keyFrameScore = getDatabaseScore(data1["feature"][1], data2["feature"][1], data2["frameList"], len(data1["frameList"]),len(data2["frameList"]))
        
        
        name = result.split("/")[-1]
        name = name.split(".")[0]
        # dis[name] = d
        
        result = SearchResult()
        result.getValue(name, keyFrameScore, d)
        results_list.append(result)
    return results_list
# query = '/Users/shaoyaqi/Downloads/576/project/output/query_interview_0.pkl'
# Label = 'interview'
# dis = compareTwoVideos(query,Label)
# print(dis)