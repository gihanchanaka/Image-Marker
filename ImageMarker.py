'''
USAGE
python ImageMarker.py FolderWithImages OutputFileName

LOADING
numpy.load(OutputFileName.npy)

'''


import argparse
import sys
import os
import cv2
import numpy as np



def mouse_callback(event, x, y, flags, params):

    if event==1:
        clicks.append([x,y])
        print(clicks)



if __name__ == "__main__":
    FOLDER=sys.argv[1]

    fileList=os.listdir(FOLDER)
    print(fileList)
    ans={}

    for f in fileList:
        ff=FOLDER+'/'+f
        print(ff)
        img=cv2.imread(ff)

        cv2.imshow("image",img)
        clicks=[]
        cv2.setMouseCallback('image', mouse_callback)
        while True:
            if len(clicks)==2:
                break
            cv2.waitKey(1)

        ans[ff]=clicks
        clicks=[]

    print(ans)
    np.save(sys.argv[2], ans)