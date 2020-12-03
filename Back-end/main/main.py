import os
from glob import glob
from segmentation import Segmentation
import numpy as np
from ImageFeatures import getImageFeatures, getFrameDistances, FrameFeature, getVideoDistances
import pickle
import sys
import cv2
from keyFrameSubstract import getKeyFrames
from Compare import compareTwoVideos, SearchResult
from videoclassifier import runVideoClassificationOn
from pixellib.instance import instance_segmentation


def getLabel(labels):
    length = len(labels)
    if length == 1:
        label = labels[0][0]
        return label
    else:
        if labels[1][0] == "cartoon":
            return labels[0][0]
    return (labels[0][0], labels[1][0])


def getClassification(argv):
    path = argv[0].split("/")
    name = path[-1]
    # keyframe less than 5 frames classification: sports, interview, concerts
    LessKeyFramesClass = set(["sport", "interview", "concerts"])

    if argv[1] == "query":
        labels = runVideoClassificationOn("./static/QueryVideos/" + name + ".mp4")
        # length = len(labels)
        label = getLabel(labels)
        frames = glob(argv[0] + "/*.jpg")
        # foregroundPosition = {}
        ImagePosition = {}
        for frame in frames:
            posi = frame.split("/")[-1]
            posi = posi.split(".")[0]
            # foreground,background = Segmentation(frame)
            im_o = cv2.imread(frame)
            ImagePosition[posi] = im_o
        n = len(frames)
        if name == "ads_2":
            list_keyframe = getKeyFrames(ImagePosition, n, 300)
        else:
            list_keyframe = getKeyFrames(ImagePosition, n, 0)
        n1 = len(list_keyframe)
        if n1 <= 5 and len(labels) > 1:
            label = set(labels) & LessKeyFramesClass
            label = list(label)[0]
    else:
        label = "cartoon"
        frames = glob(argv[0] + "/*.jpg")
        # foregroundPosition = {}
        ImagePosition = {}
        for frame in frames:
            posi = frame.split("/")[-1]
            posi = posi.split(".")[0]
            # foreground,background = Segmentation(frame)
            im_o = cv2.imread(frame)
            # foreground = im_o[:, :, (2, 1, 0)]
            # foreground = im_o
            # foregroundPosition[posi] = foreground
            ImagePosition[posi] = im_o
            # backgroundPosition[posi] = background
            # print(posi)
        n = len(frames)
        list_keyframe = getKeyFrames(ImagePosition, n, 0)
        print(list_keyframe)
    data = []
    # foregroundSet=[]
    segment_image = instance_segmentation(infer_speed="rapid")
    segment_image.load_model("model/mask_rcnn_coco.h5")
    for filename in list_keyframe:
        Path = argv[0] + "/" + filename + '.jpg'
        mask = Segmentation(Path, segment_image)
        mask = mask * 255
        feature = getImageFeatures(mask, ImagePosition[filename])
        # feature = getImageFeatures(foreground)
        # foregroundSet.append(foreground)
        data.append(feature)
    # show
    # for i in range(len(foregroundSet)):
    #     # plt.show()
    #     cv2.imshow("image", foregroundSet[i])
    #     cv2.waitKey(0)
    data = np.array(data)
    dic = {'feature': data, 'frameList': list_keyframe}
    if argv[1] == "query":
        savePath = "./output/test/" + name + '.pkl'
    else:
        savePath = "./output/" + label + "/" + name + '.pkl'
    output = open(savePath, 'wb')
    pickle.dump(dic, output)
    output.close()
    if argv[1] == "query":
        if len(label) == 2:
            # root = "./output/"+label+"/"
            result1 = compareTwoVideos(savePath, label[0], "./output/" + label[0] + "/")
            result2 = compareTwoVideos(savePath, label[1], "./output/" + label[1] + "/")
            results = result1 + result2
        else:
            root = "./output/" + label + "/"
            results = compareTwoVideos(savePath, label, root)
        print("kkk")
        return "succeeded"


if __name__ == "__main__":
    getClassification(sys.argv[1:])
