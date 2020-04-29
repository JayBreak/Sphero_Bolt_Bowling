import cv2
import numpy as np
import math

from time import sleep
from typing import Dict

from pysphero.core import Sphero
from pysphero.driving import Direction
from pysphero.driving import TankDriveDirection
from pysphero.driving import DirectionRawMotor
from pysphero.device_api.user_io import Color
from pysphero.device_api.sensor import Attitude
from pysphero.device_api.sensor import CoreTime, Quaternion, Attitude, Accelerometer, Velocity, Speed


### Camera Settings ###
frameWidth = 1280
frameHeight = 720
camBrightness = 150

### Start Capture ###
cap = cv2.VideoCapture(0) # 0 is ID of external webcam

cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, camBrightness)

### Perspectve Variables ###
width, height = 8064, 3465

pts1 = np.float32([[133, 55], [1120, 112], [97, 478], [1097, 545]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)

### Pin Color Data ###
myColors_pins = [[26, 37, 186, 60, 100, 255],  # Green Pin
                 [99, 147, 213, 108, 201, 255],  # Blue pin
                # [85, 75, 165, 125, 230, 255],  # Blue pin
                 [3, 89, 225, 13, 184, 255]]  # orange pin

### Pin Coordinate Array ###
pinCoords = [[0, 0], [0, 0], [0, 0]]

### Sphero Color Data###
myColors_sphero = [[75, 0, 255, 179, 255, 255]]  # test val

### Sphero Coordinate Array ###
roboCoords = [[0, 0]]



def findColor(img, myColors, myLocations):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    pinNum = 0
    for color, points in zip(myColors, myLocations):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        dems = getContours(mask)
        #print("fc.dems", dems)
        #cv2.circle(imgOut, (dems[0], dems[1]), 3, (255, 0, 255), cv2.FILLED)
        if dems[0] != 0 and dems[1] != 0:
            points[0] = dems[0]
            points[1] = dems[1]
        pinNum += 1
    #cv2.imshow("img", mask)


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1:
            cv2.drawContours(img, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #print(approx)
            x, y, w, h = cv2.boundingRect(approx)
            #cv2.rectangle(img, (x, y), (w + x, h + y), (0, 255, 0), 2)
            x = x + (w // 2)
            y = y + (h // 2)
        print(x, ",", y, end="\r")
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

def getPinLocation(numPull):
    while numPull > 0:
        success, img = cap.read()
        imgResult = img.copy()
        ### Setting up warp perspective ###
        imgOut = cv2.warpPerspective(img, matrix, (width, height))
        imgOut = cv2.resize(imgOut, (1344, 577))
        # cv2.imshow("warp", imgOut)
        #findColor(imgOut, myColors_sphero, roboCoords)
        findColor(imgOut, myColors_pins, pinCoords)
        #cv2.imshow("Result", imgOut)
        numPull -= 1

def getSpheroLocation(numPull):
    while numPull > 0:
        success, img = cap.read()
        imgResult = img.copy()
        ### Setting up warp perspective ###
        imgOut = cv2.warpPerspective(img, matrix, (width, height))
        imgOut = cv2.resize(imgOut, (1344, 577))
        # cv2.imshow("warp", imgOut)
        #print(myColors_sphero)
        findColor(imgOut, myColors_sphero, roboCoords)
        #cv2.imshow("Result", imgOut)
        numPull -= 1


def findangle(current,target):

    radians = math.atan2(target[1] - current[1], target[0] - current[0])
    degrees = math.degrees(radians)
    print("DONE!")
    if degrees < 0:
        degrees = 360 + degrees
    degrees = int(degrees)
    return degrees



def main():
    print("Connecting to Sphero...", end =" ")
    ### Connect to Sphero Bolt ###
    mac_address = "f7:e2:c2:7d:4c:bb"
    with Sphero(mac_address=mac_address) as sphero:
        print("DONE!")
        sphero.power.wake()
        sleep(2)
        sphero.user_io.set_all_leds_8_bit_mask()
        sleep(1)
        print("Gathering Pin Points...")
        getPinLocation(25)
        print("")
        print("DONE!")
        print("Gathering Sphero Points...")
        sphero.user_io.set_led_matrix_one_color(color=Color(blue=255))
        getSpheroLocation(25)
        print("")
        print("DONE!")
        print("pinCoords:",pinCoords)
        print("roboCoords:",roboCoords)


        ### Calibration Run ###
        angle  = 0
        start = [roboCoords[0][0], roboCoords[0][1]]
        sleep(1)
        sphero.driving.drive_with_heading(0, 0, Direction.forward)
        sleep(.75)
        sphero.driving.drive_with_heading(100, 0, Direction.forward)
        sleep(1)
        sphero.driving.drive_with_heading(0, 0, Direction.forward)
        sleep(1.25)
        oldCoords = roboCoords
        print("Gathering Sphero Points...")
        getSpheroLocation(25)
        print("")
        print("DONE!")
        print("roboCoords:",roboCoords)
        target = [roboCoords[0][0], roboCoords[0][1]]
        print("Calculating Angle...", end =" ")
        offset_angle = findangle(start,target)

        print("offset_angle:",offset_angle,"degrees")






        ### First Pin ###
        start = [roboCoords[0][0], roboCoords[0][1]]
        target = [pinCoords[0][0],pinCoords[0][1]]
        print("Calculating Angle...", end =" ")
        angle = findangle(start,target)
        angle = angle - offset_angle
        if angle < 0:
            print("its neg")
            angle = angle + 360
        sleep(1)
        print("angle:",angle,"degrees")

        print("sending command to robot...")
        sleep(.25)
        sphero.driving.drive_with_heading(0, angle, Direction.forward)
        sleep(.75)
        sphero.driving.drive_with_heading(100, angle, Direction.forward)
        sleep(2.5)
        sphero.driving.drive_with_heading(0, angle, Direction.forward)
        sleep(.25)

        ### Back up
        angle = 180
        angle = angle - offset_angle
        if angle < 0:
            print("its neg")
            angle = angle + 360
        print("sending command to robot...")
        sleep(.25)
        sphero.driving.drive_with_heading(0, angle, Direction.forward)
        sleep(.75)
        sphero.driving.drive_with_heading(100, angle, Direction.forward)
        sleep(1)
        sphero.driving.drive_with_heading(0, angle, Direction.forward)
        sleep(.75)


        ### Second Pin ###
        print("Gathering Sphero Points...")
        getSpheroLocation(25)
        print("")
        print("DONE!")
        print("roboCoords:",roboCoords)
        print("Calculating Angle...", end =" ")
        start = [roboCoords[0][0], roboCoords[0][1]]
        target = [pinCoords[1][0],pinCoords[1][1]]
        angle = findangle(start,target)
        angle = angle - offset_angle
        if angle < 0:
            print("its neg")
            angle = angle + 360
        print("angle:",angle,"degrees")

        print("sending command to robot...")
        sleep(.25)
        sphero.driving.drive_with_heading(0, angle, Direction.forward)
        sleep(.75)
        sphero.driving.drive_with_heading(100, angle, Direction.forward)
        sleep(1.25)
        sphero.driving.drive_with_heading(0, angle, Direction.forward)
        sleep(.25)

        ### Back up
        angle = 180
        angle = angle - offset_angle
        if angle < 0:
            print("its neg")
            angle = angle + 360
        print("sending command to robot...")
        sleep(.25)
        sphero.driving.drive_with_heading(0, angle, Direction.forward)
        sleep(.75)
        sphero.driving.drive_with_heading(100, angle, Direction.forward)
        sleep(1)
        sphero.driving.drive_with_heading(0, angle, Direction.forward)
        sleep(.75)

        ### Third Pin ###
        print("Gathering Sphero Points...")
        getSpheroLocation(25)
        print("")
        print("DONE!")
        print("roboCoords:",roboCoords)
        print("Calculating Angle...", end =" ")
        start = [roboCoords[0][0], roboCoords[0][1]]
        target = [pinCoords[2][0],pinCoords[2][1]]
        angle = findangle(start,target)
        angle = angle - offset_angle
        if angle < 0:
            print("its neg")
            angle = angle + 360
        print("angle:",angle,"degrees")

        print("sending command to robot...")
        sleep(.25)
        sphero.driving.drive_with_heading(0, angle, Direction.forward)
        sleep(.75)
        sphero.driving.drive_with_heading(100, angle, Direction.forward)
        sleep(1.5)
        sphero.driving.drive_with_heading(0, angle, Direction.forward)


        sphero.power.enter_soft_sleep()






if __name__ == "__main__":
    main()
