import cv2
import numpy as np
from picamera2 import Picamera2
from time import time
from _Bounds import Bounds, BoundsType

fps = 58.92
frameSize=(640,480)
camera=Picamera2()
# print(camera.sensor_modes)
camera.preview_configuration.main.size=frameSize
camera.preview_configuration.main.format="RGB888"
camera.preview_configuration.controls.FrameRate=fps     # Request 60 fps
camera.preview_configuration.align()                    # Picks closest standard size to specified size
camera.configure("preview")
camera.start()

overlayPosition = (30, 60)
overlayFont = cv2.FONT_HERSHEY_SIMPLEX
overlayFontScale = 1.5
overlayFontColor = (0, 0, 255)                          # opencv uses BGR colorspace
overlayFontThickness = 2

hueBounds = Bounds(63, 98)
saturationBounds = Bounds(100, 255)
valueBounds = Bounds(0, 51)
hsvBounds = Bounds(np.array([hueBounds.lower, saturationBounds.lower, valueBounds.lower]), np.array([hueBounds.upper, saturationBounds.upper, valueBounds.upper]))

def updateHsv():
    global hsvBounds, hueBounds, saturationBounds, valueBounds

    hsvBounds.lower = np.array([hueBounds.lower, saturationBounds.lower, valueBounds.lower])
    hsvBounds.upper = np.array([hueBounds.upper, saturationBounds.upper, valueBounds.upper])

def onHueChange(newValue, type: BoundsType, maxValue = 179):
    global hueLower, hueUpper, hueBounds
    
    if type == BoundsType.LOWER:
        if newValue > hueBounds.upper:
            hueBounds.lower = hueBounds.upper
        else:
            hueBounds.lower = newValue
    else:
        if newValue > maxValue:
            hueBounds.upper = maxValue
        elif newValue < hueBounds.lower:
            hueBounds.upper = hueBounds.lower
        else:
            hueBounds.upper = newValue
    updateHsv()

def onSaturationChange(newValue, type: BoundsType, maxValue = 255):
    global saturationLower, saturationUpper, saturationBounds
    
    if type == BoundsType.LOWER:
        if newValue > saturationBounds.upper:
            saturationBounds.lower = saturationBounds.upper
        else:
            saturationBounds.lower = newValue
    else:
        if newValue > maxValue:
            saturationBounds.upper = maxValue
        elif newValue < saturationBounds.lower:
            saturationBounds.upper = saturationBounds.lower
        else:
            saturationBounds.upper = newValue
    updateHsv()

def onValueChange(newValue, type: BoundsType, maxValue = 255):
    global valueLower, valueUpper, valueBounds
    
    if type == BoundsType.LOWER:
        if newValue > valueBounds.upper:
            valueBounds.lower = valueBounds.upper
        else:
            valueBounds.lower = newValue
    else:
        if newValue > maxValue:
            valueBounds.upper = maxValue
        elif newValue < valueBounds.lower:
            valueBounds.upper = valueBounds.lower
        else:
            valueBounds.upper = newValue
    updateHsv()

cv2.namedWindow('HSV')
cv2.createTrackbar('Hue Lower:', 'HSV', hueBounds.lower, 179, lambda newValue: onHueChange(newValue, BoundsType.LOWER))
cv2.createTrackbar('Hue Upper:', 'HSV', hueBounds.upper, 179, lambda newValue: onHueChange(newValue, BoundsType.UPPER))
cv2.createTrackbar('Saturation Lower:', 'HSV', saturationBounds.lower, 255, lambda newValue: onSaturationChange(newValue, BoundsType.LOWER))
cv2.createTrackbar('Saturation Upper:', 'HSV', saturationBounds.upper, 255, lambda newValue: onSaturationChange(newValue, BoundsType.UPPER))
cv2.createTrackbar('Value Lower:', 'HSV', valueBounds.lower, 255, lambda newValue: onValueChange(newValue, BoundsType.LOWER))
cv2.createTrackbar('Value Upper:', 'HSV', valueBounds.upper, 255, lambda newValue: onValueChange(newValue, BoundsType.UPPER))

def updateFps(newValue: float, useLowPassFilter: bool = True):
    global fps

    if useLowPassFilter:
        fps = 0.9 * fps + 0.1 * newValue
    else:
        fps = newValue

while True:
    frameStart = time()

    frame = camera.capture_array()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frameHSV, hsvBounds.lower, hsvBounds.upper)
    maskSmall = cv2.resize(mask, (int(frameSize[0] / 2), int(frameSize[1] / 2)))
    objectOfInterest = cv2.bitwise_and(frame, frame, mask=mask)
    objectOfInterestSmall = cv2.resize(objectOfInterest, (int(frameSize[0] / 2), int(frameSize[1] / 2)))
    contours, junk = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        contours = sorted(contours, key=lambda contour: cv2.contourArea(contour), reverse=True)
        # cv2.drawContours(frame, contours, 0, (255, 0, 0), 3)                                    # -1 to draw all
        biggestContour = contours[0]
        x, y, width, height = cv2.boundingRect(biggestContour)
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)
    cv2.putText(frame, str(int(fps)) + " FPS", overlayPosition, overlayFont, overlayFontScale, overlayFontColor, overlayFontThickness)

    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", maskSmall)
    cv2.imshow("Object", objectOfInterestSmall)
    if cv2.waitKey(1) == ord('q'):
        break
    frameElapsed = time() - frameStart
    updateFps(1 / frameElapsed, useLowPassFilter=True)
cv2.destroyAllWindows()
