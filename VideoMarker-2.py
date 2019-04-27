#python screen-detection-2.py ./inputFile.mp4 ./output.mp4

DEBUG=True
RESIZE_RATIO=0.3
import sys
import cv2
import numpy as np
import sklearn

import numpy as np


clicksXY=[]
finishGettingInput=False
vidIn = None
vidOut = None
frame = None

def resizedFrame(frame,ratio=RESIZE_RATIO):
    return cv2.resize(frame,(int(frame.shape[1]*ratio),int(frame.shape[0]*ratio)))


def mouse_callback(event, x, y, flags, params):
    global frame,vidIn,vidOut,clicksXY,finishGettingInput
    if event==cv2.EVENT_FLAG_LBUTTON:

        clicksXY.append([x,y])
        while len(clicksXY)>4:
            clicksXY.pop(0)
        print(x,y)

        ret,frame=readFrame(vidIn)
        assert ret, "Error in reading video"
        for i in range(len(clicksXY)):
            cv2.circle(frame,(clicksXY[i][0],clicksXY[i][1]),4,[255,255,255],thickness=4)
            cv2.line(frame,(clicksXY[i][0],clicksXY[i][1]),(clicksXY[(i+1)%len(clicksXY)][0],clicksXY[(i+1)%len(clicksXY)][1]),[255,255,255],thickness=1)

        cv2.imshow("frame",frame)
    if event==cv2.EVENT_FLAG_ALTKEY:
        finishGettingInput=True



def readFrame(vid):
    ret,frame=vid.read()
    if not ret:
        return False, None
    else:
        frame=resizedFrame(frame)
        return True, frame


def mainFunc(inputFile,outputFile,noFramesMax,randomJump):


    global frame,vidIn,vidOut,clicksXY

    vidIn=cv2.VideoCapture(inputFile)

    ret,frame=readFrame(vidIn)
    assert ret , "No frame returned"
    cv2.imshow("frame",frame)
    cv2.waitKey(10)
    cv2.setMouseCallback('frame', mouse_callback)


    X=np.zeros(shape=(noFramesMax,frame.shape[0],frame.shape[1],frame.shape[2]),dtype=np.uint8)
    Y=np.zeros((noFramesMax,4,2),dtype=np.uint32)

    f=0

    while f<noFramesMax:
        jump=np.random.randint(randomJump/2,randomJump)

        for _ in range(jump):
            ret,frame=readFrame(vidIn)
            if not ret:
                vidIn.release()
                vidIn=cv2.VideoCapture(inputFile)

        frameBackup=np.copy(frame)
        cv2.imshow("frame",frame)

        finishGettingInput=False
        while not finishGettingInput:
            cv2.waitKey(1)

        X[f]=frameBackup
        Y[f,:,:]=np.array(clicksXY)
        f+=1
        print("Frame {} of {} complete".format(f+1,noFramesMax))

    cv2.destroyWindow("frame")
    vidIn.release()


    for f in range(noFramesMax):
        frame=np.copy(X[f])
        clicksXY=Y[f]
        for i in range(len(clicksXY)):
            cv2.circle(frame,(clicksXY[i][0],clicksXY[i][1]),4,[255,255,255],thickness=4)
            cv2.line(frame,(clicksXY[i][0],clicksXY[i][1]),(clicksXY[(i+1)%len(clicksXY)][0],clicksXY[(i+1)%len(clicksXY)][1]),[255,255,255],thickness=1)


        cv2.imshow("Marked frame",frame)
        cv2.waitKey(100)










if __name__ == '__main__':
    try:
        inputFile=sys.argv[1]
        outputFile=sys.argv[2]
        noFramesMax=int(sys.argv[3])
        randomJump=int(sys.argv[4])
    except:
        print("python VideoMarker-2.py ./video/inputVid.mp4 ./dataset/screen.npz 1000")
    mainFunc(inputFile,outputFile,noFramesMax,randomJump)



