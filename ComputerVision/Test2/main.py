import cv2
from matplotlib import pyplot as plt
def print_original_image():
    image = cv2.imread('WIN_20221006_15_40_47_Pro.jpg', cv2.IMREAD_COLOR)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
def capture_webcam_image_save():
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

#print_original_image() # 원본 이미지 출력
#print_histogram() #입력 이미지 gray 전환 후 gray 이미지, 히스토그램 출력
#histogram_stretching()    #gray 이미지 전환후 히스토그램 스트레칭하여 출력
histogram_Equalization()    #gray 이미지 전환후 히스토그램 평준화하여 출력