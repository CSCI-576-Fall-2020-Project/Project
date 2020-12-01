## Color Features

### Color moment

[Color moments - Wikipedia](https://en.wikipedia.org/wiki/Color_moments)

Three main characteristics in color moment are used to represent color features: 

- Mean
  
  $E_{i} = \sum_{j=1}^{N} \frac{1}{N}p_{ij}$

- Standard Deviation
  
  $\sigma _{i} = \sqrt{\frac{1}{N}\sum_{j=1}^{N}\left ( p_{ij} - E_{i} \right )^{2}}$

- Skewness
  
  $s_{i} = \sqrt[3]{\frac{1}{N}\sum_{j=1}^{N}\left ( p_{ij} - E_{i}\right )^{3}}$

$p_{ij}$ is the value of the j-th pixel of the image at the i-th color channel.

### Texture

The Gray Level Co-occurrence Matrices (GLCM) contains the second-order statistical information of spatial relationship the pixels of an image.

Four texture features are calculated from GLCM maxtrix: Contrast, Correlation, Energy, Homogeneity

http://ijettjournal.org/volume-4/issue-6/IJETT-V4I6P194.pdf

### Color histogram

[Color histogram - Wikipedia](https://en.wikipedia.org/wiki/Color_histogram)

Color histogram represents the number of pixels that have colors in each of a fixed list of color ranges

[How-To: 3 Ways to Compare Histograms using OpenCV and Python - PyImageSearch](https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/)

## 

## Foreground Substract: Grabcut

The similarity of color features are calculated by Euclidean distance

## 

## KeyFrame Substraction

KeyFrame is defined as a frame whose inter-keyframe difference is larger than a predefined threshold

[AI-Toolbox/keyframes_extract_diff.py at master · monkeyDemon/AI-Toolbox (github.com)](https://github.com/monkeyDemon/AI-Toolbox/blob/master/preprocess%20ToolBox/keyframes_extract_tool/keyframes_extract_diff.py)
