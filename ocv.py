import cv2
import numpy as np

def nothing(x):
    pass

def getContour(img,img_cont):
    contours,_ = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
   

    for cnt in contours:
        area = cv2.contourArea(cnt)
        area_trackbar = cv2.getTrackbarPos("Area","Parameters")
        if area > area_trackbar:
            cv2.drawContours(img_cont,cnt,-1,(255,0,255),7)
            arc = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*arc,True)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5
            print(len(approx))
            if len(approx) == 4:
                x1,y1,w,h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / float(h)
                #print(aspect_ratio)
                if aspect_ratio >= 0.90 and aspect_ratio <= 1.10:
                    cv2.putText(img_cont, "Square", (x, y),
                    cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
                else:
                    cv2.putText(img_cont, "Rectangle", (x, y),
                    cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            elif len(approx) == 3:
                cv2.putText(img_cont, "Triangle", (x, y),
                cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            elif len(approx) == 5:
                cv2.putText(img_cont, "Pentagon", (x, y),
                cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            elif len(approx) == 10:
                cv2.putText(img_cont, "Star", (x, y),
                cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            else:
                cv2.putText(img_cont, "Circle", (x, y),
                cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
        

# Enable camera
url_mates = 'http://192.168.0.147:8081'
url_marek = 'http://192.168.1.12:8080/video'
cap = cv2.VideoCapture(url_mates)

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshhold1","Parameters",22,255,nothing)
cv2.createTrackbar("Threshhold2","Parameters",210,225,nothing)
cv2.createTrackbar("Area","Parameters",0,30000,nothing)

while True:
    ret, frame = cap.read()
    temp = cv2.resize(frame,(640,480))

    resize = temp[150:150+330, 0:0+640]
    
    if frame is None:
        print("cam je odpojena")
        break
    img_cont = resize.copy()
    
    img_gs_blur = cv2.GaussianBlur(resize,(7,7),1)
    img_gray = cv2.cvtColor(img_gs_blur,cv2.COLOR_BGR2GRAY)


    threshhold1 = cv2.getTrackbarPos("Threshhold1","Parameters")
    threshhold2 = cv2.getTrackbarPos("Threshhold2","Parameters")
    img_canny = cv2.Canny(img_gray,threshhold1,threshhold2)

    # zvyraznenie hran v canny filt
    kernel = np.ones((5,5))
    img_dilatation = cv2.dilate(img_canny,kernel,iterations=1)

    # kontury
    getContour(img_dilatation,img_cont)
    cv2.imshow("Mask",img_dilatation)
    cv2.imshow("Original",img_cont)


    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()