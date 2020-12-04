from numpy.lib.histograms import histogram
from skimage.color import rgb2hsv, rgb2gray
import numpy as np
from skimage.feature.texture import greycomatrix, greycoprops
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances
from skimage import io
import cv2
import math

GREYLEVEL = 256
NUM_BIN = 16

class FrameFeature:
    def __init__(self, hist, moment, glcm):
        self.hist = hist
        self.moment = moment
        self.glcm = glcm
    
# Used in ColorMoments
def skewness(x, mask, mean):
    n = mask.shape[0]
    m = mask.shape[1]
    sum = 0
    cnt = 0
    for i in range(n):
        for j in range(m):
            if mask[i][j] == 255:
                cnt += 1
                sum += (x[i][j] - mean) **3
    tmp = sum / cnt
    return np.sign(tmp) * abs(tmp) ** (1/3)

def getImageFeatures(mask, img_bgr):
    # Histogram
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([img_bgr],[0, 1, 2], mask, [NUM_BIN, NUM_BIN, NUM_BIN], [0,256, 0, 256, 0, 256]) #3D histogram
    data_hist = cv2.normalize(hist, hist).flatten()
    
    # Color moment
    data_moment = np.zeros([9])
    for j in range(3):
        channel = img_rgb[:, :, j] /255
        mean, stddev = cv2.meanStdDev(channel, mask = mask)
        mean = mean[0]
        stddev = stddev[0]
        
        data_moment[j] = mean
        data_moment[j + 3] = stddev
        data_moment[j + 6] = skewness(channel, mask, mean)
    
    # GLCM
    grey_img = rgb2gray(img_rgb)
    grey_img = (grey_img*255).astype('uint8')

    glcm = greycomatrix(grey_img, distances=[1], angles=[0, 90], levels=GREYLEVEL, symmetric= True, normed= True)
    glcm_contrast = greycoprops(glcm, 'contrast') / ((GREYLEVEL-1) ** 2) # normalized contrast
    glcm_correlation = greycoprops(glcm, 'correlation')
    glcm_energy = greycoprops(glcm, 'energy')
    glcm_homogeneity = greycoprops(glcm, 'homogeneity')
    
    data_glcm = np.concatenate((glcm_contrast, glcm_correlation, glcm_energy, glcm_homogeneity), axis= 1)[0]
    
    return FrameFeature(data_hist, data_moment, data_glcm)
    # hist's shape: (4096,)
    # moment's shape: (9,)
    # GLCM's shape (8,)
    

def getFrameDistances(feature1, feature2):
    d_hist = euclidean_distances(feature1.hist.reshape(1,-1), feature2.hist.reshape(1,-1))
    # d_hist = 0
    d_glcm = euclidean_distances(feature1.glcm.reshape(1,-1), feature2.glcm.reshape(1,-1))
    # d_glcm = 0
    d_moment = euclidean_distances(feature1.moment.reshape(1,-1), feature2.moment.reshape(1,-1))
    # d_moment = 0
    d = math.sqrt(d_hist ** 2 + d_glcm ** 2 + d_moment ** 2)
    return d
    
# n = min(len(list1_keyFrames), len(list2_keyFrames))
#data1 id query
def getVideoDistances(dataList1, dataList2, n):
    d = 0
    shift = 0
    for i in range(n):
        d += getFrameDistances(dataList1[i], dataList2[i+shift])
    return d / n

def getNearstDistances(dataList1, dataList2, n1, n2):
    d_sum = 0
    # shift = 0
    
    for i in range(n1):
        dis_min = math.inf
        for j in range(n2):
            d = getFrameDistances(dataList1[i], dataList2[j])
            if dis_min>d:
                dis_min = d
        d_sum+=dis_min
    return d_sum / n1
    
def getDatabaseScore(dataList1, dataList2, dataFrameList2, n1, n2):
    score_key_frame={}
    # shift = 0
    for i in range(n2):
        dis_min = math.inf
        for j in range(n1):
            d = getFrameDistances(dataList1[j], dataList2[i])
            if dis_min>d:
                dis_min = d
        # d_sum+=dis_min
        score_key_frame[dataFrameList2[i]] = dis_min
        
    return score_key_frame
    