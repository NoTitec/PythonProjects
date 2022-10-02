import cv2

#image=cv2.imread('fruit_512c.jpg',cv2.IMREAD_COLOR)
#cv2.imshow("Image",image)

#cv2.waitKey(0)

capture=cv2.VideoCapture(0)
wth=capture.get(cv2.CAP_PROP_FRAME_WIDTH)
hit=capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('Frame width {},height{}'.format(wth,hit))

fourcc=cv2.VideoWriter_fourcc(*'DIVX')
video=cv2.VideoWriter('20191320 권순혁.avi',fourcc,30.0,(640,480))


while(cv2.waitKey(32)<0):
    ret,frame=capture.read()
    if not ret:
        break

    cv2.imshow("Frame",frame)

    video.write(frame)

capture.release()
video.release()