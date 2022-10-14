import cv2
import numpy as np
from imutils.video import VideoStream
from yolodetect import YoloDetect

class Start_Video:
    def __init__(self):
        self.video = VideoStream(src=1).start()
    # Chua cac diem nguoi dung chon de tao da giac
        self.points = []

    # new model Yolo
        self.model = YoloDetect()
        self.detect = False

    # def handle_left_click(event, x, y, flags, points):
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         points.append([x, y])
    #         with open("point.txt","a",encoding="utf8") as p:
    #             p.write(str(x)+" "+str(y)+"\n")


    def get_points(self):
        with open("point.txt","r") as p:
            data = p.read().split("\n")

        for d in data :
            x = d.split(" ")[0]
            y = d.split(" ")[1]
            self.points.append([int(x), int(y)])

    def draw_polygon (self,frame, points):
        for point in points:
            frame = cv2.circle( frame, (point[0], point[1]), 5, (0,0,255), -1)

        frame = cv2.polylines(frame, [np.int32(points)], False, (255,0, 0), thickness=2)
        return frame

    def main(self):    

        while True:
            frame = self.video.read()
            frame = cv2.flip(frame, 1)

            # Ve ploygon
            frame = self.draw_polygon(frame, self.points)

            if self.detect:
                frame = self.model.detect(frame= frame, points= self.points)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('d'):
                self.get_points()
                self.points.append(self.points[0])
                self.detect = True

            # Hien anh ra man hinh
            cv2.imshow("Intrusion Warning", frame)

            # cv2.setMouseCallback('Intrusion Warning', handle_left_click, points)

        self.video.stop()
        cv2.destroyAllWindows()
