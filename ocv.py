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
                if aspect_ratio >= 0.70 and aspect_ratio <= 1.30:
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
        


def get_greyscale_mask(image):
    img_gs_blur = cv2.GaussianBlur(resize,(7,7),1)
    img_gray = cv2.cvtColor(img_gs_blur,cv2.COLOR_BGR2GRAY)


    threshhold1 = cv2.getTrackbarPos("Threshhold1","Parameters")
    threshhold2 = cv2.getTrackbarPos("Threshhold2","Parameters")
    img_canny = cv2.Canny(img_gray,threshhold1,threshhold2)

    # zvyraznenie hran v canny filt
    kernel = np.ones((5,5))
    img_dilatation = cv2.dilate(img_canny,kernel,iterations=1)

    return img_dilatation

def get_hsv_mask(image):

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

    return mask

# Enable camera
url_mates = 'http://192.168.0.147:8081'
url_marek = 'http://192.168.1.11:8080/video'
cap = cv2.VideoCapture(url_marek)

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshhold1","Parameters",22,255,nothing)
cv2.createTrackbar("Threshhold2","Parameters",210,225,nothing)
cv2.createTrackbar("Area","Parameters",0,30000,nothing)

cv2.namedWindow("TB")
cv2.createTrackbar("L-H", "TB", 0 , 180, nothing)
cv2.createTrackbar("L-S", "TB", 68 , 255, nothing)
cv2.createTrackbar("L-V", "TB", 154 , 255, nothing)
cv2.createTrackbar("U-H", "TB", 180 , 180, nothing)
cv2.createTrackbar("U-S", "TB", 255 , 255, nothing)
cv2.createTrackbar("U-V", "TB", 255 , 255, nothing)

prd = 0

while True:
    ret, frame = cap.read()
    temp = cv2.resize(frame,(640,480))

    resize = temp[150:150+330, 0:0+640]
    
    if frame is None:
        print("cam je odpojena")
        break
    img_cont = resize.copy()
    

    if prd == 0: 
        img_dil = get_greyscale_mask(resize)
    if prd == 1:
        img_dil = get_hsv_mask(resize)



    # kontury
    getContour(img_dil,img_cont)
    cv2.imshow("Mask",img_dil)
    cv2.imshow("Original",img_cont)


    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == 30:
        prd = 0
    if key == 31:
        prd = 1
        


cap.release()
cv2.destroyAllWindows()