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
def skewness(x):
    tmp = np.mean((x - x.mean()) ** 3)
    return np.sign(tmp) * abs(tmp) ** (1/3)

def getImageFeatures(rgb_img):
    # Histogram
    # img_bgr = cv2.imread(filePath)
    img_bgr = rgb_img
    hist = cv2.calcHist([img_bgr],[0, 1, 2], None, [NUM_BIN, NUM_BIN, NUM_BIN], [0,256, 0, 256, 0, 256]) #3D histogram
    data_hist = cv2.normalize(hist, hist).flatten()
    
    # Color moment
    # rgb_img = io.imread(filePath)
    # hsv_img = rgb2hsv(rgb_img)
    
    data_moment = np.zeros([9])
    for j in range(3):
        channel = rgb_img[:, :, j] /255
        data_moment[j] = channel.mean()
        data_moment[j + 3] = channel.std()
        data_moment[j + 6] = skewness(channel)
    
    # GLCM
    grey_img = rgb2gray(rgb_img)
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
def getNearstDistances(dataList1, dataList2, n1,n2):
    d_sum = 0
    # shift = 0
    dis_min = 100000
    for i in range(n1):
        for j in range(n2):
            d = getFrameDistances(dataList1[i], dataList2[j])
            if dis_min>d:
                dis_min = d
        d_sum+=dis_min
    return d / n1
    