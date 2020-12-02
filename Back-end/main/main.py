import os
from glob import glob
from segmentation import Segmentation
import numpy as np
from ImageFeatures import getImageFeatures, getFrameDistances, FrameFeature, getVideoDistances
import pickle
import sys
import cv2
from keyFrameSubstract import getKeyFrames
from Compare import compareTwoVideos
def main(argv):
    label = "interview"
    path = argv[0].split("/")
    name = path[-1]
    frames = glob(argv[0]+"/*.jpg")
    foregroundPosition = {}
    # backgroundPosition = {}
    for frame in frames:
        posi = frame.split("/")[-1]
        posi = posi.split(".")[0]
        # foreground,background = Segmentation(frame)
        im_o = cv2.imread(frame)
        foreground = im_o[:, :, (2, 1, 0)]
        foregroundPosition[posi] = foreground
        # backgroundPosition[posi] = background
        # print(posi)
    n = len(frames)
    list_keyframe = getKeyFrames(foregroundPosition,n)
    data = []
    for filename in list_keyframe:
        Path = argv[0]+"/"+filename+'.jpg'
        foreground,background = Segmentation(Path)
        # feature = getImageFeatures(foregroundPosition[filename])
        feature = getImageFeatures(foreground)
        data.append(feature)
    data = np.array(data)
    dic = {'feature': data, 'frameList': list_keyframe}
    if argv[1]=="query":
        savePath = "./output/test/"+name+'.pkl'
    else:
        savePath = "./output/"+label+"/"+name+'.pkl'
    output = open(savePath, 'wb')
    pickle.dump(dic, output)
    output.close()
    if argv[1]=="query":
        root = "./output/"+label+"/"
        dis = compareTwoVideos(savePath,label,root)
        print(dis)
main(sys.argv[1:])
