## Video Classification
***This directory was forked from this [project](https://www.pyimagesearch.com/2019/07/15/video-classification-with-keras-and-deep-learning/).***

### How to run this project.

1. Train your model for 50 epochs: ```python train.py --dataset Sports-Type-Classifier/data --model model/activity.model \
	--label-bin output/lb.pickle --epochs 50```
2. You can test your model with: ```python predict_video.py --model model/activity.model \
	--label-bin model/lb.pickle \
	--input example_clips/test.mp4 \
	--output output/output.avi \
	--size 1```