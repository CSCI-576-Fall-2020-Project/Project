import os
from glob import glob
import pickle
from main import getLabel
from Compare import compareTwoVideos
import sys
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