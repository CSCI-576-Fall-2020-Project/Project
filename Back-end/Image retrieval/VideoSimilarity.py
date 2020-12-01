from keyFrameSubstract import getKeyFrames
from ImageFeatures import getImageFeatures, getDistances
import os

# PATH1 is the location of query video
PATH1 = "D:/CS Courses/CS 576/Project/Data_jpg/ads/ads_1"

PATH2 = "D:/CS Courses/CS 576/Project/Data_jpg/ads/ads_2"
list1_keyFrames = getKeyFrames(PATH1)
list2_keyFrames = getKeyFrames(PATH2)

n = min(len(list1_keyFrames), len(list2_keyFrames))
d = 0
for i in range(n):
    pathFrame1 = os.path.join(PATH1, list1_keyFrames[i])
    pathFrame2 = os.path.join(PATH2, list2_keyFrames[i])
    d += getDistances(getImageFeatures(pathFrame1), getImageFeatures(pathFrame2))
return d / n



