import numpy as np
import cv2
g_image = cv2.imread('WIN_20221006_15_40_47_Pro.jpg', cv2.IMREAD_GRAYSCALE)

ret, b_image = cv2.threshold(g_image, 128, 255, cv2.THRESH_BINARY)

morph_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))


di_image1 = cv2.dilate(b_image, morph_rect, iterations=1)
er_image1 = cv2.erode(b_image, morph_rect, iterations=2)
mp_image1 = cv2.morphologyEx(b_image, cv2.MORPH_OPEN, morph_rect, iterations=4)

cv2.imshow('Gray image', g_image)
cv2.imshow('Diletion image - rect iter 1', di_image1)
cv2.imshow('Erosion image - rect iter 2', er_image1)
cv2.imshow('Opening image - rect iter 4', mp_image1)


cv2.waitKey(0)