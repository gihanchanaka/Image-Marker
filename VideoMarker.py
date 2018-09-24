'''
USAGE
python VideoMarker.py FolderWithImages OutputFileName

NOTE : LEFT CLICK for one end and RIGHT CLICK for the other
Keep pressing ENTER to continue. If you want to stop at the middle press 'q'

LOADING
numpy.load(OutputFileName.npy)

'''


import argparse
import sys
import os
import cv2
import numpy as np


def mouse_callback(event, x, y, flags, param):
    global frame
    if event == cv2.EVENT_RBUTTONDOWN:
        points[2], points[3] = x, y
        frame1 = np.array(frame, copy=True)
        cv2.rectangle(frame1,(points[0],points[1]),(points[2],points[3]),(0,255,0),3)
        cv2.imshow('frame', frame1)
        # print(x, y, points)
    if event == cv2.EVENT_LBUTTONDOWN:
        points[0], points[1] = x, y
        frame1 = np.array(frame, copy=True)
        cv2.rectangle(frame1,(points[0],points[1]),(points[2],points[3]),(0,255,0),3)
        cv2.imshow('frame', frame1)
        # print(x, y, points)



if __name__ == "__main__":
    FILE_NAME=sys.argv[1]

    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', mouse_callback)

    cap = cv2.VideoCapture(FILE_NAME)
    ans = []
    points = [0, 0, 0, 0]

    while (1):
        ret, frame = cap.read()
        if ret == True:

            frame1 = np.array(frame, copy = True)
            cv2.rectangle(frame1, (points[0], points[1]), (points[2], points[3]), (0, 255, 0), 2)
            cv2.imshow('frame', frame1)

            k = cv2.waitKey(0) & 0xff
            if k == ord('q'):
                break

            print (points)
            x1, y1, x2, y2 = points
            points[0] = min(x1, x2)
            points[1] = min(y1, y2)
            points[2] = max(x1, x2)
            points[3] = max(y1, y2)

            ans.append(points)


    print("Saved")
    np.save(sys.argv[2], ans)
