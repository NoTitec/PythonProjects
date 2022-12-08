import cv2
import numpy as np
from matplotlib import pyplot as plt
def print_original_image():
    image = cv2.imread('WIN_20221006_15_40_47_Pro.jpg', cv2.IMREAD_COLOR)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
def save_video_first_frame():
    video=cv2.VideoCapture('videoresource/20191320 권순혁_Threshold.avi')

    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('videoresource/orginimage.jpg', gray)

def save_Thresholding_Dilation_Erosion_Opening():
    image = cv2.imread('videoresource/orginimage.jpg', cv2.IMREAD_GRAYSCALE)
    morph_elip = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilate_frame = cv2.dilate(image, morph_elip, iterations=1)
    erosion_frame=cv2.erode(image,morph_elip,iterations=1)
    opening_frame=cv2.morphologyEx(image,cv2.MORPH_OPEN,morph_elip,iterations=1)
    cv2.imwrite('videoresource/delateimage.jpg', dilate_frame)
    cv2.imwrite('videoresource/erosionimage.jpg', erosion_frame)
    cv2.imwrite('videoresource/openingimage.jpg', opening_frame)
def Dilation_video_show():
    video=cv2.VideoCapture('videoresource/20191320 권순혁_Threshold.avi')
    morph_elip=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

    while (cv2.waitKey(32) < 0):
        ret, frame = video.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #변환
        trance_frame=cv2.dilate(gray,morph_elip,iterations=1)
        cv2.imshow("result", trance_frame)
def capture_webcam_image_save():
    capture=cv2.VideoCapture(0)
    wth=capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    hit=capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('Frame width {},height{}'.format(wth,hit))

    fourcc=cv2.VideoWriter_fourcc(*'DIVX')
    video = cv2.VideoWriter('20191320 권순혁_coin_video.avi', fourcc, 30.0, (640, 480), isColor=False)

    while(cv2.waitKey(32)<0):
        ret,frame=capture.read()
        if not ret:
            break
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        cv2.imshow("Frame",gray)

        video.write(gray)

    capture.release()
    video.release()
def video_Thresholding_filtering():
    video=cv2.VideoCapture('20191320 권순혁.avi')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    thresholdvideo = cv2.VideoWriter('20191320 권순혁_Threshold.avi', fourcc, 30.0, (640, 480),False)
    while(cv2.waitKey(32)<0):
        ret,frame=video.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        tret,os_frame=cv2.threshold(gray,128,255,cv2.THRESH_OTSU)
        if not tret:
            print("error")
        cv2.imshow("result",os_frame)
        thresholdvideo.write(os_frame)
    video.release()
    thresholdvideo.release()

def video_Sobel_filtering():
    video = cv2.VideoCapture('20191320 권순혁.avi')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    sobelvideo = cv2.VideoWriter('20191320 권순혁_Sobel.avi', fourcc, 30.0, (640, 480), False)
    while (cv2.waitKey(32) < 0):
        ret, frame = video.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        s_videoXY=cv2.Sobel(gray,cv2.CV_8U,1,1,ksize=3)
        n_image = cv2.normalize(s_videoXY, None, 0, 255, cv2.NORM_MINMAX)
        cv2.imshow("result",n_image)
        sobelvideo.write(n_image)
    video.release()
    sobelvideo.release()

def video_Canny_filtering():
    video = cv2.VideoCapture('20191320 권순혁.avi')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    cannyvideo = cv2.VideoWriter('20191320 권순혁_Canny.avi', fourcc, 30.0, (640, 480), False)
    while (cv2.waitKey(32) < 0):
        ret, frame = video.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cannyframe=cv2.Canny(gray,10,50)
        #n_image = cv2.normalize(s_videoXY, None, 0, 255, cv2.NORM_MINMAX)
        cv2.imshow("result",cannyframe)
        cannyvideo.write(cannyframe)
    video.release()
    cannyvideo.release()

def video_hough_transform():
    video = cv2.VideoCapture('20191320 권순혁.avi')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    hough_video = cv2.VideoWriter('20191320 권순혁_Hough.avi', fourcc, 30.0, (640, 480), False)
    while (cv2.waitKey(32) < 0):
        ret, frame = video.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurframe=cv2.blur(gray,(5,5))
        cannyframe=cv2.Canny(blurframe,50,150)
        lines=cv2.HoughLines(cannyframe,1,np.pi/180,100)
        scale=frame.shape[0]+frame.shape[1]
        for line in lines:
            rho,theta=line[0]
            a=np.cos(theta)
            b=np.sin(theta)
            x0=a*rho
            y0=b*rho
            x1=int(x0+scale*(-b))
            y1=int(y0+scale*(a))
            x2=int(x0-scale*(-b))
            y2=int(y0-scale*(a))
            cv2.line(gray,(x1,y1),(x2,y2),(255,0,255),1)
            cv2.imshow("line",gray)
        hough_video.write(gray)
    video.release()
    hough_video.release()


def two_video_to_one():
    video = cv2.VideoCapture('20191320 권순혁.avi')
    video2 = cv2.VideoCapture('20191320 권순혁_Hough.avi')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    two_video = cv2.VideoWriter('20191320 권순혁_Origin_Hough.avi', fourcc, 30.0, (1280, 480), False)
    while (cv2.waitKey(32) < 0):
        ret, frame = video.read()
        ret2, frame2 = video2.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        concate_horizontalframe=cv2.hconcat([gray,gray2])
        cv2.imshow("concat_result",concate_horizontalframe)
        two_video.write(concate_horizontalframe)
    video.release()
    two_video.release()
def print_histogram():
    o_image=cv2.imread('WIN_20221006_15_40_47_Pro.jpg')
    g_image=cv2.cvtColor(o_image,cv2.COLOR_BGR2GRAY)
    g_hist=cv2.calcHist([g_image],[0],None,[256],[0,256])

    plt.title('Histogram')
    plt.plot(g_hist,color='black')

    cv2.imshow('Gray Image',g_image)
    plt.show()
    cv2.waitKey(0)

def histogram_stretching():
    o_image = cv2.imread('WIN_20221006_15_40_47_Pro.jpg')
    g_image = cv2.cvtColor(o_image, cv2.COLOR_BGR2GRAY)

    #stretching
    n_image=cv2.normalize(g_image,None,0,255,cv2.NORM_MINMAX)

    g_hist=cv2.calcHist([g_image],[0],None,[256],[0,256])
    n_hist=cv2.calcHist([n_image],[0],None,[256],[0,256])

    plt.title('Histogram Stretching')
    plt.plot(g_hist,color='gray')
    plt.plot(n_hist,color='blue')

    cv2.imshow('Stretch image',n_image)
    plt.show()
    cv2.waitKey(0)

def histogram_Equalization():
    o_image = cv2.imread('WIN_20221006_15_40_47_Pro.jpg')
    g_image = cv2.cvtColor(o_image, cv2.COLOR_BGR2GRAY)

    #equlization
    n_image=cv2.equalizeHist(g_image)

    g_hist = cv2.calcHist([g_image], [0], None, [256], [0, 256])
    n_hist = cv2.calcHist([n_image], [0], None, [256], [0, 256])

    plt.title('Histogram Equlization')
    plt.plot(g_hist, color='gray')
    plt.plot(n_hist, color='blue')

    cv2.imshow('Equalization image',n_image)
    plt.show()

    cv2.waitKey(0)

def avg_filtering():
    o_image = cv2.imread('WIN_20221006_15_40_47_Pro.jpg')
    g_image = cv2.cvtColor(o_image, cv2.COLOR_BGR2GRAY)

    #avg_filter
    avg_image=cv2.blur(g_image,(5,5))
    cv2.imshow('origin image',g_image)
    cv2.imshow('Average filtered image',avg_image)
    cv2.waitKey(0)

def Gaussian_filtering():
    o_image = cv2.imread('WIN_20221006_15_40_47_Pro.jpg')
    g_image = cv2.cvtColor(o_image, cv2.COLOR_BGR2GRAY)

    #Gaussian_filtering
    gau_image=cv2.GaussianBlur(g_image,(5,5),0)
    cv2.imshow('Gaussian filtered image', gau_image)
    cv2.waitKey(0)

def Median_filtering():
    o_image = cv2.imread('WIN_20221006_15_40_47_Pro.jpg')
    g_image = cv2.cvtColor(o_image, cv2.COLOR_BGR2GRAY)

    #Medianfilter
    m_image=cv2.medianBlur(g_image,5)
    cv2.imshow('Median filtered image',m_image)
    cv2.waitKey(0)
def high_hartz_filtering():
    o_image = cv2.imread('WIN_20221006_15_40_47_Pro.jpg')
    g_image = cv2.cvtColor(o_image, cv2.COLOR_BGR2GRAY)

    #high_filter
    kernel=np.array([[0,-1,0],
                    [-1,4,-1],
                    [0,-1,0]])

    h_image=cv2.filter2D(g_image,-1,kernel)
    cv2.imshow('high filter image',h_image)
    cv2.waitKey(0)

def Circle_hough_transform():
    video = cv2.VideoCapture('20191320 권순혁_coin_video.avi')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    circlevideo = cv2.VideoWriter('20191320 권순혁_circlefind.avi', fourcc, 30.0, (640, 480))
    while (cv2.waitKey(32) < 0):
        ret, frame = video.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,1500,param1=250,param2=10,minRadius=24,maxRadius=31)

        for i in circles[0]:
            cv2.circle(frame,(int(i[0]),int(i[1])),2,(255,0,0),2)
            cv2.circle(frame,(int(i[0]),int(i[1])),int(i[2]),(0,0,255),5)


        cv2.imshow("result", frame)
        circlevideo.write(frame)
    video.release()
    circlevideo.release()

def Harris_Corner_transform():
    video = cv2.VideoCapture('20191320 권순혁.avi')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    harrisvideo = cv2.VideoWriter('20191320 권순혁_hirris.avi', fourcc, 30.0, (640, 480),False)
    while (cv2.waitKey(32) < 0):
        ret, frame = video.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corner=cv2.cornerHarris(gray,2,3,0.04)

        coord=np.where(corner>0.05*corner.max())
        coord=np.stack((coord[1],coord[0]),axis=-1)

        for(x,y) in coord:
            cv2.circle(gray,(x,y),5,(0,0,255),1,cv2.LINE_AA)

        #harrisframe=cv2.normalize(corner,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)

        cv2.imshow("result", gray)
        harrisvideo.write(gray)
    video.release()
    harrisvideo.release()

def SIFT_transform():
    video = cv2.VideoCapture('20191320 권순혁.avi')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    SIFTvideo = cv2.VideoWriter('20191320 권순혁_SIFT.avi', fourcc, 30.0, (640, 480))
    while (cv2.waitKey(32) < 0):
        ret, frame = video.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sift_detector=cv2.xfeatures2d.SIFT_create()
        keypoints,descriptor=sift_detector.detectAndCompute(gray,None)
        ov_image=cv2.drawKeypoints(frame,keypoints,None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow("result", ov_image)
        SIFTvideo.write(ov_image)
    video.release()
    SIFTvideo.release()

def Region_Labeling():
    originimage=cv2.imread('coins.bmp',cv2.IMREAD_UNCHANGED)
    grayimage=cv2.cvtColor(originimage,cv2.COLOR_BGR2GRAY)
    gau_image = cv2.GaussianBlur(grayimage, (7, 7), 0)
    tret, os_frame = cv2.threshold(gau_image, 0, 255, cv2.THRESH_OTSU)

    morph_elip = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))

    erosion_frame = cv2.erode(os_frame, morph_elip, iterations=1)
    cv2.imshow('erosion',erosion_frame)

    cnt, labels = cv2.connectedComponents(erosion_frame)

    print("erosion total count={}".format(cnt))

    cv2.waitKey(0)

def Watershed_Mouse_Click():
    image=cv2.imread('WIN_20221006_15_40_47_Pro',cv2.IMREAD_UNCHANGED)
    (hit,wth)=image.shape[0:2]

    marker=np.zeros((hit,wth),np.int32)
    marker_id=1
    colors=[]

    w_image=image.copy()

def onMouse(event,x,y,flags,param):
    image = cv2.imread('WIN_20221006_15_40_47_Pro', cv2.IMREAD_UNCHANGED)
    (hit, wth) = image.shape[0:2]

    marker = np.zeros((hit, wth), np.int32)
    marker_id = 1
    colors = []

    w_image = image.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        marker[y,x]=marker_id
        colors.append((marker_id,image[y,x]))
        cv2.circle(w_image,(x,y),3,(0,0,255),-1)
        cv2.imshow('image',w_image)
        marker_id+=1

    elif event ==cv2.EVENT_RBUTTONDOWN:
        cv2.watershed(image,marker)
        w_image[marker==-1]=(0,0,255)
        for m_id,color in colors:
            w_image[marker==m_id]=color
        cv2.imshow('watershed',w_image)

    cv2.imshow('image',image)

    cv2.setMouseCallback('image',onMouse())
    cv2.waitKey(0)
#print_original_image() # 원본 이미지 출력
#capture_webcam_image_save()# 웹캠 graysacle 영상 촬영 저장
#video_Thresholding_filtering()
#video_Sobel_filtering()
#print_histogram() #입력 이미지 gray 전환 후 gray 이미지, 히스토그램 출력
#histogram_stretching()    #gray 이미지 전환후 히스토그램 스트레칭하여 출력
#histogram_Equalization()    #gray 이미지 전환후 히스토그램 평준화하여 출력
#avg_filtering()
#Gaussian_filtering()
#high_hartz_filtering()
#Median_filtering()
#video_Canny_filtering()
#video_hough_transform()
#two_video_to_one()
#save_video_first_frame()
#Dilation_video_show()
#save_Thresholding_Dilation_Erosion_Opening()
#Circle_hough_transform()
#Harris_Corner_transform()
#SIFT_transform()
#Region_Labeling()

onMouse()