import cv2
import numpy as np
import serial


# 연동
arduino = serial.Serial('COM3', 9600)  # 아두이노에 연결하는 객체
cap = cv2.VideoCapture(0)
# 전역변수
width = 0
height = 0
key=102
while (True):
    #get frame
    ret, frame = cap.read()
    #blur with Gaussian
    blurframe = cv2.GaussianBlur(frame, (15, 15), 0)
    #trans to hsv
    hsv_frame = cv2.cvtColor(blurframe, cv2.COLOR_BGR2HSV)
    if ret:
        print("*" * 50)
        # print("frame(y, x, color):", img.shape)
        # print("frame size:", img.size, "type:", img.dtype)
        width = hsv_frame.shape[1]
        height = hsv_frame.shape[0]
        #get center x,y
        cx=int(width/2)
        cy=int(height/2)
        #print center hsv
        pixel_center=hsv_frame[cy,cx]
        hue_value=pixel_center[0]
        print("huevalue is")
        print(hue_value)
        print("*******")
        key=ord('f')
        if(hue_value<5):
            key=ord('g')
            arduino.write(b'f\n')
            print("red")
            print(key)
        elif (hue_value < 22):
            arduino.write(b'r\n')
            print("orange")
        elif (hue_value < 33):
            arduino.write(b'r\n')
            print("yellow")
        elif(hue_value<78):
            key=ord('f')
            arduino.write(b'l\n')
            print("green")
            print(key)
        elif(hue_value<131):
            key=ord('i')
            arduino.write(b's\n')
            print("blue")
            print(key)
        elif(hue_value < 170):
            arduino.write(b'b\n')
            print("violet")
        #draw circle on blurframe
        cv2.circle(blurframe,(cx,cy),5,(255,0,0),3)
        print("*" * 50)

    cv2.imshow('frame', blurframe)

    key = cv2.waitKey(1) & 0xFF  # 키보드 입력 이벤트 발생시 진입
    if(key==115): # s입력시 정지
        print(key)
        arduino.write([115])
        break
    # 기본적으로는 계속 key에 f 전달 r색상이면 g 이면 f b 이면 i key에 저장

    # ord 함수는 하나의 문자를 인자로 받고 해당 문자에 해당하는 유니코드 정수를 반환합니다.

   # if key == ord('f'):  # 전진
   #     #arduino.write(key)
   #     print(key)
   # elif key == ord('g'):  # 왼쪽 전진
   #     #arduino.write(key)
   #     print(key)
   # elif key == ord('i'):  # 오른쪽 전진
   #     #arduino.write(key)
   #     print(key)

cap.release()
cv2.destroyAllWindows()


# enum {
#   GOFORWARD = 'f',
#   GOBACKWARD = 'b',
#   TURNLEFT = 'l',
#   TURNRIGHT = 'r',
#   STOP = 's',
#   GOFORWARDLEFT = 'g',
#   GOFORWARDRIGHT = 'i',
#   GOBACKWARDLEFT = 'h',
#   GOBACKWARDRIGHT = 'j',
# }; /*SERIAL*/
#
# enum {
#   SPEED_0 = '0',
#   SPEED_1 = '1',
#   SPEED_2 = '2',
#   SPEED_3 = '3',
#   SPEED_4 = '4',
#   SPEED_5 = '5',
#   SPEED_6 = '6',
#   SPEED_7 = '7',
#   SPEED_8 = '8',
#   SPEED_9 = '9',
#   SPEED_10 = 'q',
# }; /*SPEED*/
#
# enum {
#   FRONTLIGHTON = 'W',
#   FRONTLIGHTOFF = 'w',
#   REARLIGHTON = 'U',
#   REARLIGHTOFF = 'u',
#   ALLLIGHTON = 'A',
#   ALLLIGHTOFF = 'a',
#   REARLEFTBLINK = 'z',
#   REARRIGHTBLINK = 'c',
# }; /*LIGHT*/

