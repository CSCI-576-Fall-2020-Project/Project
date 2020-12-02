# Back-end Description

## Flow Chart

<img src="https://user-images.githubusercontent.com/55118568/100811021-8a45df00-33ee-11eb-8fc1-eca53412087e.jpeg" width="600">

## Video Labeling

This part is mainly refered from [this article](https://www.pyimagesearch.com/2019/07/15/video-classification-with-keras-and-deep-learning/).

The CNN model **ResNet-50** is trained using Keras for image classification.

## Foreground Separation

Foreground and background is separated by Instance segmentation in [PixelLib](https://github.com/ayoolaolafenwa/PixelLib) library. Instance segmentation with PixelLib is based on MaskRCNN framework.

## Keyframe Substraction

The Keyframe in a video is defined as a frame whose inter-keyframe difference is larger than a predefined threshold

[AI-Toolbox/keyframes_extract_diff.py at master · monkeyDemon/AI-Toolbox (github.com)](https://github.com/monkeyDemon/AI-Toolbox/blob/master/preprocess%20ToolBox/keyframes_extract_tool/keyframes_extract_diff.py)

## Color Features

**Color moment**

[Color moments - Wikipedia](https://en.wikipedia.org/wiki/Color_moments)

Three main characteristics in color moment are used to represent color features: 

- Mean

- Standard Deviation

- Skewness

**Texture**

The Gray Level Co-occurrence Matrices (GLCM) contains the second-order statistical information of spatial relationship the pixels of an image.

Four texture features are calculated from GLCM maxtrix: 

- Contrast

- Correlation

- Energy

- Homogeneity

http://ijettjournal.org/volume-4/issue-6/IJETT-V4I6P194.pdf

**Color histogram**

[Color histogram - Wikipedia](https://en.wikipedia.org/wiki/Color_histogram)

Color histogram represents the number of pixels that have colors in each of a fixed list of color ranges

[How-To: 3 Ways to Compare Histograms using OpenCV and Python - PyImageSearch](https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/)

## Video Similarity

The similarity of color features are calculated by the average Euclidean distance of keyframe's feature vector between query video and video in the database.
