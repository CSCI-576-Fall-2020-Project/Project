import os
from glob import glob
from segmentation import Segmentation
import numpy as np
from ImageFeatures import getImageFeatures, getFrameDistances, FrameFeature, getVideoDistances
import pickle
import sys
import cv2
from keyFrameSubstract import getKeyFrames
from Compare import compareTwoVideos,SearchResult
from videoclassifier import runVideoClassificationOn
from pixellib.instance import instance_segmentation

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
        return ["concerts"]
        

def getClassification(argv):
    path = argv[0].split("/")
    name = path[-1]
    isQuery = argv[1]=="query"

    labels = getLabel(isQuery, name)
        
    frames = glob(argv[0]+"/*.jpg")
    # foregroundPosition = {}
    ImagePosition = {}
    for frame in frames:
        posi = frame.split("/")[-1]
        posi = posi.split(".")[0]
        # foreground,background = Segmentation(frame)
        im_o = cv2.imread(frame)
        # foreground = im_o[:, :, (2, 1, 0)]
        foreground = im_o
        # foregroundPosition[posi] = foreground
        ImagePosition[posi] = im_o
        # backgroundPosition[posi] = background
        # print(posi)
    n = len(frames)
    list_keyframe = getKeyFrames(ImagePosition,n)
    print(list_keyframe)
    
    data = [[], []]
    # foregroundSet=[]
    # segment_image = instance_segmentation(infer_speed = "rapid")
    # segment_image.load_model("/Users/shaoyaqi/Downloads/576/project/mask_rcnn_coco.h5")
    
    for filename in list_keyframe:
        Path = argv[0]+"/"+filename+'.jpg'
        mask = Segmentation(Path)
        mask_255 = np.ones(mask.shape, np.uint8)*255

        feature_background = getImageFeatures(mask,ImagePosition[filename])
        feature_fullimage = getImageFeatures(mask_255,ImagePosition[filename])
        # feature = getImageFeatures(foreground)
        # foregroundSet.append(foreground)
        data[0].append(feature_background)
        data[1].append(feature_fullimage)
        print(filename)
        
    #show
    # for i in range(len(foregroundSet)):
    #     # plt.show()
    #     cv2.imshow("image", foregroundSet[i])
    #     cv2.waitKey(0)
    
    data = np.array(data)
    dic = {'feature': data, 'frameList': list_keyframe}
    
    if isQuery:
        savePath = "./output/test/" + name + '.pkl'
    else:
        savePath = "./output/" + labels[0] +"/"+ name + '.pkl'
    output = open(savePath, 'wb')
    pickle.dump(dic, output)
    output.close()
    
    results = []
    if isQuery:
        for label in labels:
            root = "./output/"+label+"/"
            results += compareTwoVideos(savePath,label,root)
        
        for result in results:
            print(result.videoName)
            print(result.totalScore)
            print(result.keyFrames)
    return results

if __name__ == "__main__":
    # PATH = "D:/CS Courses/CS 576/Project/query/test_jpg/concert_1"
    # getClassification([PATH, "query"])
    getClassification(sys.argv[1:])