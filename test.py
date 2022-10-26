""" Created by MrBBS """
# 2/10/2022
# -*-encoding:utf-8-*-

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from face_detection.face_detect import FaceDetection
import numpy as np
import cv2
import time

face_det = FaceDetection()
# mask_det = MaskDetection()

cap = cv2.VideoCapture(0)
last_t = time.time()
while True:
    fps = 0
    try:
        t = time.time()
        fps = 1 / (t - last_t)
        last_t = t
    except:
        pass
    ret, frame = cap.read()
    if ret is None:
        break
    for (x1, y1, x2, y2), face in face_det.get_face(frame):
        cv2.imshow('cc', face)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, ((x1+x2)//2,(y1+y2)//2), 5, (0, 255, 0), -1)
    cv2.putText(frame, f'FPS: {fps}', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2)
    cv2.imshow('cam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
