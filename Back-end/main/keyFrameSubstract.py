from collections import abc
import os
import numpy as np
import cv2

# def getKeyFrames(filesPath):
#     filename = os.listdir(filesPath)
#     filename.sort(key=lambda x: int(os.path.splitext(x)[0][5:]))
#     n = len(filename)
    
#     frame_cur = None
#     frame_prev = None
#     list_diff = []
#     for i in range(n):
#         filePath = filesPath + "/" + filename[i]
#         img_bgr = cv2.imread(filePath)
#         img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
#         frame_cur = img_rgb
#         if frame_prev is not None:
#             diff = cv2.absdiff(frame_cur, frame_prev)
#             cnt_diff = np.sum(diff)
#             list_diff.append((i, cnt_diff, filename[i]))
#             #跟前一关键帧相比
#         frame_prev = frame_cur
    
#     list_diff = sorted(list_diff, key = lambda x: x[1], reverse=True)
            
#     list_keyframe = []
#     for tup in list_diff:
#         if tup[1] > 20000000:
#             list_keyframe.append(tup)
    
#     list_keyframe.append((0, 0, filename[0]))
#     list_keyframe = sorted(list_keyframe, key = lambda x: x[0])
#     ret = []
#     for tup in list_keyframe:
#         ret.append((tup[2], tup[0]))
#         print(tup[2])
#     return ret

def getKeyFrames(filesDict,n):
    # filename = os.listdir(filesPath)
    # filename.sort(key=lambda x: int(os.path.splitext(x)[0][5:]))
    # n = len(filename)
    
    frame_cur = None
    frame_prev = None
    list_diff = []
    Key = list(filesDict.keys())
    Key.sort(key=lambda x: int(x[5:]))
    # key = sorted(list(key))
    for i in range(n):
        # filePath = filesPath + "/" + filename[i]
        filename = Key[i]
        # if int(filename[5:])>=480 and int(filename[5:])<960:
        if int(filename[5:])<=480:
        # print(filename)
            img_bgr = filesDict[filename]
            img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            frame_cur = img_hsv[:,:,0]
            
            if i > 0:
                #Compare current frame with last keyframe
                diff = cv2.absdiff(frame_cur, frame_prev)
                cnt_diff = np.sum(diff)
                if cnt_diff > 7500000:
                    list_diff.append((i, cnt_diff, filename))
                    frame_prev = frame_cur
            else:
                list_diff.append((i, 0, filename))
                frame_prev = frame_cur
    
    
    list_keyframe = sorted(list_diff, key = lambda x: x[0])
    ret = []
    for tup in list_keyframe:
        # ret.append((tup[2], tup[0]))
        ret.append(tup[2])
    return ret
        

if __name__ == "__main__":
    PATH = "D:/CS Courses/CS 576/Project/Data_jpg"
    
    f = open("./keyframe.txt", 'w+')
    for root, dirs, files in os.walk(PATH):
        for dir in dirs:
            if len(os.listdir(os.path.join(root, dir))) > 10:
                filesPath = os.path.join(root, dir)
                print(filesPath, file=f)
                ret = getKeyFrames(filesPath)
                print(ret, file=f)
     