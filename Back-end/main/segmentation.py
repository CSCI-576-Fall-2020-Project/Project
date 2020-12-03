import pixellib
from pixellib.instance import instance_segmentation
from matplotlib import pyplot as plt
import cv2
import numpy as np
from pixellib.semantic import semantic_segmentation
def Segmentation(imagePath,segment_image):
    segmask, _ = segment_image.segmentImage(imagePath)
    # segment_image.segmentImage("./Data_jpg/sport/sport_0/frame0.jpg", show_bboxes = True, output_image_name = "image_new3.jpg")
    # segmask, _ = segment_image.process_video(imagePath)
    
    # capture = cv2.VideoCapture(0)
    # segment_video = instance_segmentation(infer_speed = "rapid")
    # segment_video.load_model("mask_rcnn_coco.h5")
    # segment_video.process_camera(capture, frames_per_second= 10, output_video_name="output_video.mp4", show_frames= True,
    # frame_name= "frame")

    mask = segmask['masks']
    # plt.imshow(output)
    # plt.show()
    im_o = cv2.imread(imagePath)
    img = im_o[:, :, (2, 1, 0)]
    if mask.shape[-1]==0:
        Mask0 = np.ones(img.shape,np.uint8)
        return Mask0
    total_mask = np.where((mask[:,:,0]==1),1,0).astype('uint8')
    for i in range(1,mask.shape[-1]):
        mask1 = mask[:,:,i]
        mask1 = np.array(mask1)
        total_mask = np.where((total_mask==1)|(mask1==1),1,0).astype('uint8')

    # background = (1-total_mask[:,:,np.newaxis])*img
    # plt.imshow(background) 
    # plt.show()
    # foreground = (total_mask[:,:,np.newaxis])*img
    # plt.show()
    # cv2.imshow("image", foreground)
    # cv2.waitKey(0)
    # cv2.destroyWindow()
    Mask0 = np.zeros(img.shape,np.uint8)
    Mask0[:,:,0] = total_mask
    Mask0[:,:,1] = total_mask
    Mask0[:,:,2] = total_mask
    return Mask0
# Segmentation('./Data_jpg/ads/ads_0/frame505.jpg')
# Segmentation("/Users/shaoyaqi/Downloads/576/project/")