import cv2
import numpy as np

image=cv2.imread('WIN_20221006_15_40_47_Pro.jpg',cv2.IMREAD_UNCHANGED)
(hit,wth)=image.shape[0:2]

marker=np.zeros((hit,wth),np.int32)
marker_id=1
colors=[]
w_image=image.copy()

def onMouse(event,x,y,flags,param):

    global marker
    global marker_id
    global colors

    if event == cv2.EVENT_LBUTTONDOWN:
        marker[y,x]=marker_id
        colors.append((marker_id,image[y,x]))
        cv2.circle(w_image,(x,y),3,(0,0,255),-1)
        cv2.imshow('image',w_image)
        marker_id=marker_id+1

    elif event ==cv2.EVENT_RBUTTONDOWN:
        cv2.watershed(image,marker)
        w_image[marker==-1]=(0,0,255)
        for m_id,color in colors:
            w_image[marker==m_id]=color
        cv2.imshow('watershed',w_image)

cv2.imshow('image',image)

cv2.setMouseCallback('image',onMouse)
cv2.waitKey(0)