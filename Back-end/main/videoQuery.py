import os
from glob import glob
import pickle
# from main import getLabel
from Compare import compareTwoVideos
from videoclassifier import runVideoClassificationOn
import sys
def getLabel(isQuery, videoName):
    
    #keyframe less than 5 frames classification: sports, interview, concerts
    # LessKeyFramesClass = set(["sport","interview","concerts"])
    
    if isQuery:
        labels = runVideoClassificationOn("./static/QueryVideos/"+videoName+".mp4")
        # length = len(labels)
        
        labelList = []
        for label in labels:
            labelList.append(label[0])
            
        # Hardcode Exception
        if set(labelList) == set(["ads", "cartoon"]):
            labelList = ["ads"]
        if set(labelList) == set(["ads", "movies"]):
            labelList = ["movies"]
        if set(labelList) == set(["movies", "interview"]):
            labelList = ["interview"]
        return labelList
    else:
        return ["interview"]
def videoQuery(argv):
    path = argv[0].split("/")
    name = path[-1]
    labels = getLabel(True, name)
    results = []
    savePath = "./output/test/" + name + '.pkl'
    for label in labels:
        root = "./output/"+label+"/"
        results += compareTwoVideos(savePath,label,root)
    return results
if __name__ == "__main__":
    # PATH = "D:/CS Courses/CS 576/Project/query/test_jpg/concert_1"
    # videoQuery([PATH]  
    videoQuery(sys.argv[1:])