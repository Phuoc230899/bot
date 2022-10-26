from re import L
from tabnanny import check
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import cv2
import numpy as np
import datetime
import threading
from speech import hello
from face_detection.face_detect import FaceDetection




def isInside(points, centroid):
    polygon = Polygon(points)
    centroid = Point(centroid)
    print(polygon.contains(centroid))
    return polygon.contains(centroid)

def notInside(points, centroid):
    if isInside(points,centroid):
        return False
    return True
# def isInside(x,y,point):
#     if x in range(point[0][0], point[1][0]) and y in range(point[0][1], point[1][1]):
#         return True
#     else :
#         return False


class YoloDetect():
    def __init__(self, detect_class="person", frame_width=1080, frame_height=920):
        # Parameters
        self.first_detect = None
        self.play_index = 0
        self.check_face = 0
        self.face_det = FaceDetection()
        self.time_reset = True


    def draw_prediction(self, img,x, y, x_plus_w, y_plus_h, points,centroid):
        if isInside(points,centroid):
            if self.first_detect == None :
                self.first_detect = datetime.datetime.utcnow()
            img = self.alert(img)
        return isInside(points,centroid)

    def alert(self, img):
        cv2.putText(img, "ALARM!!!!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if round((datetime.datetime.utcnow() - self.first_detect).total_seconds()) > 5 and self.play_index<1:
            speech = threading.Thread(target =hello,args=("Xin chào anh chị",))
            speech.start()
            self.play_index +=1
            self.time_reset = False

    def reset(self):
        self.play_index = 0
        self.first_detect = None
        self.time_reset = True

    def detect(self, frame, points):
        # blob = cv2.dnn.blobFromImage(frame, self.scale, (416, 416), (0, 0, 0), True, crop=False)
        # self.model.setInput(blob)
        # outs = self.model.forward(self.output_layers)

        # # Loc cac object trong khung hinh
        # class_ids = []
        # confidences = []
        # boxes = []

        # for out in outs:
        #     for detection in out:
        #         scores = detection[5:]
        #         class_id = np.argmax(scores)
        #         confidence = scores[class_id]
        #         if (confidence >= self.conf_threshold) and (self.classes[class_id] == self.detect_class):
        #             center_x = int(detection[0] * self.frame_width)
        #             center_y = int(detection[1] * self.frame_height)
        #             w = int(detection[2] * self.frame_width)
        #             h = int(detection[3] * self.frame_height)
        #             x = center_x - w / 2
        #             y = center_y - h / 2
        #             class_ids.append(class_id)
        #             confidences.append(float(confidence))
        #             boxes.append([x, y, w, h])

        # indices = cv2.dnn.NMSBoxes(boxes, confidences, self.conf_threshold, self.nms_threshold)

        # for i in indices:
        #     box = boxes[i]
        #     print(box)
        #     x = box[0]
        #     y = box[1]
        #     w = box[2]
        #     h = box[3]
        #     self.draw_prediction(frame, class_ids[i], round(x), round(y), round(x + w), round(y + h), points)
        if self.first_detect !=None:
            if round((datetime.datetime.utcnow() - self.first_detect).total_seconds()) > 7 and self.time_reset == True:
                self.first_detect = None
        for (x1, y1, x2, y2), face in self.face_det.get_face(frame):
            centroid = ((x1+x2)//2,(y1+y2)//2)
            self.draw_prediction(frame,x1, y1, x1 + x2, y1 + y2, points,centroid)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, ((x1+x2)//2,(y1+y2)//2), 5, (0, 255, 0), -1)
        return frame