from re import L
from tabnanny import check
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import cv2
import numpy as np
# from telegram_utils import send_telegram
import datetime
import threading
from speech import hello
def isInside(points, centroid):
    polygon = Polygon(points)
    centroid = Point(centroid)
    print(polygon.contains(centroid))
    return polygon.contains(centroid)


class YoloDetect():
    def __init__(self, detect_class="person", frame_width=1080, frame_height=920):
        # Parameters
        self.classnames_file = "model/classnames.txt"
        self.weights_file = "model/yolov4-tiny.weights"
        self.config_file = "model/yolov4-tiny.cfg"
        self.conf_threshold = 0.5
        self.nms_threshold = 0.4
        self.detect_class = detect_class
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = 1 / 255
        self.model = cv2.dnn.readNet(self.weights_file, self.config_file)
        self.classes = None
        self.output_layers = None
        self.read_class_file()
        self.get_output_layers()
        self.last_alert = None
        self.alert_telegram_each = 15  # seconds
        self.play_index = 0
        self.face_cascade = cv2. CascadeClassifier('haarcascade_frontalface_default.xml')
        self.check_face = 0

    def read_class_file(self):
        with open(self.classnames_file, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

    def get_output_layers(self):
        layer_names = self.model.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.model.getUnconnectedOutLayers()]

    def draw_prediction(self, img, class_id, x, y, x_plus_w, y_plus_h, points):
        # label = str(self.classes[class_id])
        color = (0, 255, 0)
        a=0
        b=0
        c=0
        d=0
        # cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
        # cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray,1.1,4)
        # if len(faces) == 0:
        #     self.play_index = 0
        #     self.last_alert = None
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            a=x
            b=y
            c=x+w
            d=y+h
            print(a,b,c,d)
        # Tinh toan centroid
        centroid = ((a + c) // 2, (b + d) // 2)
        cv2.circle(img, centroid, 5, (color), -1)
        if self.last_alert != None:
            if round((datetime.datetime.utcnow() - self.last_alert).total_seconds()) > 10:
                self.play_index = 0
                self.last_alert = None
        if isInside(points, centroid):
            if self.last_alert == None :
                self.last_alert = datetime.datetime.utcnow()
            img = self.alert(img)
            # if self.play_index <= 1 and self.play_index >0 :
                # thread = threading.Thread(target=hello)
                # thread.start()
                # thread.join()
                
            # if round((datetime.datetime.utcnow() - self.last_alert).total_seconds()) > 5:
            #     if isInside(points, centroid) and self.play_index<1: 
            #         hello()
            #         self.play_index+=1
                
            #     if not isInside(points, centroid):
            #         self.play_index=0
            #         self.last_alert=None

            # if round((datetime.datetime.utcnow() - self.last_alert).total_seconds()) > 20:
            #     self.play_index = 0
            #     self.last_alert = None
        return isInside(points, centroid)

    def alert(self, img):
        cv2.putText(img, "ALARM!!!!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if round((datetime.datetime.utcnow() - self.last_alert).total_seconds()) > 5 and self.play_index<1:
            hello("Xin Chào Anh Chị")
            self.play_index +=1
            self.last_alert = None



    def detect(self, frame, points):
        blob = cv2.dnn.blobFromImage(frame, self.scale, (416, 416), (0, 0, 0), True, crop=False)
        self.model.setInput(blob)
        outs = self.model.forward(self.output_layers)

        # Loc cac object trong khung hinh
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if (confidence >= self.conf_threshold) and (self.classes[class_id] == self.detect_class):
                    center_x = int(detection[0] * self.frame_width)
                    center_y = int(detection[1] * self.frame_height)
                    w = int(detection[2] * self.frame_width)
                    h = int(detection[3] * self.frame_height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.conf_threshold, self.nms_threshold)

        for i in indices:
            box = boxes[i]
            print(box)
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            self.draw_prediction(frame, class_ids[i], round(x), round(y), round(x + w), round(y + h), points)

        return frame