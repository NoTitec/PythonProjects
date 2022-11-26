import cv2
import serial

# 연동
arduino = serial.Serial('COM3', 9600)
cap = cv2.VideoCapture(0)

while (True):
    ret, frame = cap.read()

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('a'):  # 왼쪽
        arduino.write(b'l\n')
        print(b'l\n')
    elif key == ord('d'):  # 오른쪽
        arduino.write(b'r\n')
        print(b'r\n')
    elif key == ord('w'):  # 위
        arduino.write(b'f\n')
        print(b'f\n')
    elif key == ord('s'):  # 아래
        arduino.write(b'b\n')
        print(b'b\n')

cap.release()
cv2.destroyAllWindows()

