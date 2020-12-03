from collections import abc
import os
import numpy as np
import cv2

def getKeyFrames(filesDict,n,N1):
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
        if int(filename[5:])<=480+N1:
            # print(filename)
            img_bgr = filesDict[filename]
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            frame_cur = img_rgb
            
            if i > 0:
                #Compare current frame with last keyframe
                diff = cv2.absdiff(frame_cur, frame_prev)
                cnt_diff = np.sum(diff)
                if cnt_diff > 23000000*1.5:
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
        

# if __name__ == "__main__":
#     PATH = "D:/CS Courses/CS 576/Project/Data_jpg"
    
#     f = open("./keyframe.txt", 'w+')
#     for root, dirs, files in os.walk(PATH):
#         for dir in dirs:
#             if len(os.listdir(os.path.join(root, dir))) > 10:
#                 filesPath = os.path.join(root, dir)
#                 print(filesPath, file=f)
#                 ret = getKeyFrames(filesPath)
#                 print(ret, file=f)
     