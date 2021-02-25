import cv2
import numpy as np

def nothing(x):
    pass


# Enable camera
cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    white = np.ones((img.shape[0], img.shape[1], 3))

    for c in contours:
        approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
        cv2.drawContours(img, [approx], 0, (0, 255, 0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 3:
            cv2.putText(img, "Triangle", (x, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        elif len(approx) == 4:
            x1, y1, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / float(h)
            print(aspect_ratio)
            if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
                cv2.putText(img, "Square", (x, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            else:
                cv2.putText(img, "Rectangle", (x, y),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        elif len(approx) == 5:
            cv2.putText(img, "Pentagon", (x, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        elif len(approx) == 10:
            cv2.putText(img, "Star", (x, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        else:
            cv2.putText(img, "Circle", (x, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

    cv2.imshow("imgGry",thrash)
    cv2.imshow("img",img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()