import cv2
import numpy as np
import math

### Camera Settings ###
frameWidth = 1280
frameHeight = 720
camBrightness = 150

cap = cv2.VideoCapture(0)

cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, camBrightness)

### Perspectve Variables ###
width, height = 8064, 3465

pts1 = np.float32([[133, 55], [1120, 112], [97, 478], [1097, 545]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)

myColors_pins = [[26, 37, 186, 60, 100, 255],  # Green Pin
                 [99, 147, 213, 108, 201, 255],  # Blue pin
                 [3, 89, 225, 13, 184, 255]]  # orange pin

pinCoords = [[0, 0], [0, 0], [0, 0]]

# myColors_sphero = [[0,0,255,179,83,255]]       #Sphero-white
#myColors_sphero = [[0, 0, 255, 165, 18, 255]]  # test val
myColors_sphero = [[75, 0, 255, 179, 255, 255]]  # test val


roboCoords = [[0, 0], [0, 0], [0, 0]]


def findColor(img, myColors, myLocations):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    pinNum = 0
    for color, points in zip(myColors, myLocations):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        dems = getContours(mask)
        cv2.circle(img, (dems[0], dems[1]), 3, (255, 0, 255), cv2.FILLED)
        if dems[0] != 0 and dems[1] != 0:
            myLocations[0] = dems[0]
            myLocations[1] = dems[1]
        pinNum += 1
    # cv2.imshow("img", mask)


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1:
            cv2.drawContours(imgOut, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            if x is None:
                x, y, w, h = 0, 0, 0, 0
                print("NONE")
            cv2.rectangle(imgOut, (x, y), (w + x, h + y), (0, 255, 0), 2)
            x = x + (w // 2)
            y = y + (h // 2)
        print(x, ",", y)
    return x, y, w, h


def findNextPin(pinCoords, roboCoords):
    num = 0
    count = 0
    short_dist = 0
    for pin in pinCoords:
        dist = math.sqrt((pin[1] - pin[0])**2 + (roboCoords[0][1] - roboCoords[0][0])**2)
        if short_dist == 0:
            short_dist = dist
            num = count
        elif short_dist <= dist:
            short_dist = dist
            num = count
        count += 1
    return num


while True:
    success, img = cap.read()
    imgResult = img.copy()
    ### Setting up warp perspective ###
    imgOut = cv2.warpPerspective(img, matrix, (width, height))
    imgOut = cv2.resize(imgOut, (1344, 577))
    cv2.imshow("warp", imgResult)

    findColor(imgOut, myColors_pins, pinCoords)
    findColor(imgOut, myColors_sphero, roboCoords)
    cv2.imshow("Result", imgOut)

    #nextPin = findNextPin(pinCoords, roboCoords)
    #print("Closest Pin:",nextPin)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
