# USAGE
# python predict_video.py --model model/activity.model --label-bin model/lb.pickle --input example_clips/lifting.mp4 --output output/lifting_128avg.avi --size 128

# import the necessary packages
from tensorflow.keras.models import load_model
from collections import deque
import numpy as np
import pickle
import cv2


def runVideoClassificationOn(video_directory):
    vc_results = {}
    model = load_model("model/activity.model")
    lb = pickle.loads(open("output/lb.pickle", "rb").read())

    # initialize the image mean for mean subtraction along with the
    # predictions queue
    mean = np.array([123.68, 116.779, 103.939][::1], dtype="float32")
    Q = deque(maxlen=128)

    # initialize the video stream, pointer to output video file, and
    # frame dimensions
    vs = cv2.VideoCapture(video_directory)
    writer = None
    (W, H) = (None, None)

    # loop over frames from the video file stream
    while True:
        # read the next frame from the file
        (grabbed, frame) = vs.read()

        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break

        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        # clone the output frame, then convert it from BGR to RGB
        # ordering, resize the frame to a fixed 224x224, and then
        # perform mean subtraction
        output = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (224, 224)).astype("float32")
        frame -= mean

        # make predictions on the frame and then update the predictions
        # queue
        preds = model.predict(np.expand_dims(frame, axis=0))[0]
        Q.append(preds)

        # perform prediction averaging over the current history of
        # previous predictions
        results = np.array(Q).mean(axis=0)
        i = np.argmax(results)
        label = lb.classes_[i]
        if label not in vc_results.keys():
            vc_results[label] = 1
        else:
            vc_results[label] += 1
        results = []
        for k in vc_results.keys():
            results.append((k, vc_results[k]))
        results = sorted(results, key=lambda a: a[1], reverse=True)
    print("[INFO] cleaning up...")
    vs.release()
    return results[0:2]


print(runVideoClassificationOn("mp4/ads_1.mp4"))
