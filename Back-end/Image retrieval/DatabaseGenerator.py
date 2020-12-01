import os
import numpy as np
from ImageFeatures import getImageFeatures, getFrameDistances, FrameFeature, getVideoDistances
import pickle
from keyFrameSubstract import getKeyFrames

def saveData(filePath):
    list_keyframe = getKeyFrames(filePath)
    n = len(list_keyframe)
    data = []
    for i in range(n):
        data.append(getImageFeatures(filePath + "/" + list_keyframe[i]))
            
    d = getVideoDistances(data, data, len(list_keyframe))
    dict = {'feature': data, 'frameList': list_keyframe}

    output = open('myfile.pkl', 'wb')
    pickle.dump(dict, output)
    output.close()

# pkl_file = open('myfile.pkl', 'rb')
# mydict2 = pickle.load(pkl_file)
# pkl_file.close()


# query_hist, query_feature = getImageFeatures("2.jpg");

# minv = float("inf")
# ret = 0
# for i in range(len(data_feature)):
#     d = getDistances((query_hist, query_feature), (data_hist[i], data_feature[i]))
#     if (d < minv):
#         minv = d
#         ret = i

if __name__ == "__main__":
    PATH = "D:/CS Courses/CS 576/Project/Data_jpg/ads/ads_1"
    saveData(PATH)
    
    
     