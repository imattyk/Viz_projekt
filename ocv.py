import cv2
import numpy as np

def nothing(x):
    pass

# Enable camera
cap = cv2.VideoCapture(0)

cv2.namedWindow("TB")
cv2.createTrackbar("L-H", "TB", 0 , 180, nothing)
cv2.createTrackbar("L-S", "TB", 68 , 255, nothing)
cv2.createTrackbar("L-V", "TB", 154 , 255, nothing)
cv2.createTrackbar("U-H", "TB", 180 , 180, nothing)
cv2.createTrackbar("U-S", "TB", 255 , 255, nothing)
cv2.createTrackbar("U-V", "TB", 255 , 255, nothing)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # frame je RGB tak ho prevediem na HSV

    l_h = cv2.getTrackbarPos("L-H","TB")
    l_s = cv2.getTrackbarPos("L-S","TB")
    l_v = cv2.getTrackbarPos("L-V","TB")

    u_h = cv2.getTrackbarPos("U-H","TB")
    u_s = cv2.getTrackbarPos("U-S","TB")
    u_v = cv2.getTrackbarPos("U-V","TB")

    low_red = np.array([l_h,l_s,l_v])
    upper_red = np.array([u_h,u_s,u_v])
    mask = cv2.inRange(hsv,low_red,upper_red)


    # contours

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # prefiltrovat obraz
    kernel = np.ones((5,5),np.uint8) 
    mask = cv2.erode(mask,kernel)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if area > 400:
            cv2.drawContours(frame,[approx], 0,(0,0,0),5)


    cv2.imshow("Frame",frame)
    cv2.imshow("Mask",mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()