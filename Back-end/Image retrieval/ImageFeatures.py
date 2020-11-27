from numpy.lib.histograms import histogram
from skimage.color import rgb2hsv, rgb2gray
import numpy as np
from skimage.feature.texture import greycomatrix, greycoprops
from skimage import io
import cv2

GREYLEVEL = 256

# Used in ColorMoments
def skewness(x):
    tmp = np.mean((x - x.mean()) ** 3)
    return np.sign(tmp) * abs(tmp) ** (1/3)

def getImageFeatures(filePath):
    
    img_bgr = cv2.imread(filePath)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([img_bgr],[0, 1, 2], None, [64, 64, 64], [0,256, 0, 256, 0, 256]) #3D histogram
    hist = cv2.normalize(hist, hist).flatten()
    
    
    rgb_img = io.imread(filePath)
    hsv_img = rgb2hsv(rgb_img)
    
    
    
    # color moment
    data_1d = np.zeros([9])
    for j in range(3):
        channel = hsv_img[:, :, j]
        
        hist = np.histogram(rgb_img[:, :, j], bins = 256, range=(0, 256))
        
        data_1d[j] = channel.mean()
        data_1d[j + 3] = channel.std()
        data_1d[j + 6] = skewness(channel)
    
    # GLCM
    grey_img = rgb2gray(rgb_img)
    grey_img = (grey_img*255).astype('uint8')

    glcm = greycomatrix(grey_img, distances=[1], angles=[0, 90], levels=GREYLEVEL, symmetric= True, normed= True)
    glcm_contrast = greycoprops(glcm, 'contrast') / ((GREYLEVEL-1) ** 2) # normalized contrast
    glcm_correlation = greycoprops(glcm, 'correlation')
    glcm_energy = greycoprops(glcm, 'energy')
    glcm_homogeneity = greycoprops(glcm, 'homogeneity')
    
    ret = np.concatenate((data_1d.reshape(1,-1), glcm_contrast, glcm_correlation, glcm_energy, glcm_homogeneity), axis= 1)
    
    return hist, ret
