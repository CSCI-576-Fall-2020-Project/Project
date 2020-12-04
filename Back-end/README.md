# Back-end Description

## Flow Chart

<img src="https://user-images.githubusercontent.com/55118568/101194598-0d477f00-3613-11eb-95ea-1c67eae88a97.jpeg" width="600">

## Video Labeling

This part is mainly refered from [this article](https://www.pyimagesearch.com/2019/07/15/video-classification-with-keras-and-deep-learning/).

The CNN model **ResNet-50** is trained using Keras for image classification.

## Keyframe Substraction

The Keyframe in a video is defined as a frame whose inter-frame difference is larger than a predefined threshold

## Foreground Separation

Foreground and background is separated by Instance segmentation in [PixelLib](https://github.com/ayoolaolafenwa/PixelLib) library. Instance segmentation in PixelLib is based on MaskRCNN framework.

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

## Video Similarity

The similarity of videos is calculated by the average Euclidean distance of keyframe's feature vector between query video and the videos in the database.
