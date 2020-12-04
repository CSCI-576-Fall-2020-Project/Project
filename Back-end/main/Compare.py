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
        self.queryKeyFrames = {}
        self.dataKeyFrames = {}
    def getValue(self,Name,Score1,Score2,d):
        self.videoName = Name
        self.queryKeyFrames = Score1
        self.totalScore = d
        self.dataKeyFrames = Score2
def compareTwoVideos(query,label,root):
    
    pkl_file1 = open(query, 'rb')
    data1 = pickle.load(pkl_file1)
    if label=="cartoon":
        data1["feature"] = [data1["feature"],data1["feature"]]
    # dataPath = '/Users/shaoyaqi/Downloads/576/project/output/'+Label 
    database = glob(root+"/*.pkl")
    dis = {}
    results_list=[]
    for result in database:
        pkl_file2 = open(result, 'rb')
        data2 = pickle.load(pkl_file2)
        if label=="cartoon":
            data2["feature"] = [data2["feature"],data2["feature"]]
        # d = getVideoDistances(data1["feature"],data2["feature"],min(len(data1["frameList"]),len(data2["frameList"])))
        
        d_foreground = getNearstDistances(data1["feature"][0],data2["feature"][0],len(data1["frameList"]),len(data2["frameList"]))
        d_fullimage = getNearstDistances(data1["feature"][1],data2["feature"][1],len(data1["frameList"]),len(data2["frameList"]))
        
        if d_foreground < d_fullimage:
            d = d_foreground
            datakeyFrameScore = getDatabaseScore(data1["feature"][0], data2["feature"][0], data2["frameList"], len(data1["frameList"]),len(data2["frameList"]))
        else: 
            d = d_fullimage
            datakeyFrameScore = getDatabaseScore(data1["feature"][1], data2["feature"][1], data2["frameList"], len(data1["frameList"]),len(data2["frameList"]))
        
        d_foreground = getNearstDistances(data2["feature"][0],data1["feature"][0],len(data2["frameList"]),len(data1["frameList"]))
        d_fullimage = getNearstDistances(data2["feature"][1],data1["feature"][1],len(data2["frameList"]),len(data1["frameList"]))
        
        if d_foreground < d_fullimage:

            querykeyFrameScore = getDatabaseScore(data2["feature"][0], data1["feature"][0], data1["frameList"], len(data2["frameList"]),len(data1["frameList"]))
        else: 

            querykeyFrameScore = getDatabaseScore(data2["feature"][1], data1["feature"][1], data1["frameList"], len(data2["frameList"]),len(data1["frameList"]))
        
        name = result.split("/")[-1]
        name = name.split(".")[0]
        # dis[name] = d
        
        result = SearchResult()
        result.getValue(name,querykeyFrameScore,datakeyFrameScore,d)
        results_list.append(result)
    return results_list
# query = '/Users/shaoyaqi/Downloads/576/project/output/query_interview_0.pkl'
# Label = 'interview'
# dis = compareTwoVideos(query,Label)
# print(dis)