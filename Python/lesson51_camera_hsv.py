import cv2
import numpy as np
from picamera2 import Picamera2
from time import time

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

hueRange = (10, 50)
saturationRange = (100, 255)
valueRange = (100, 255)
hsvLowerBounds = np.array([hueRange[0], saturationRange[0], valueRange[0]])
hsvUpperBounds = np.array([hueRange[1], saturationRange[1], valueRange[1]])

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
    mask = cv2.inRange(frameHSV, hsvLowerBounds, hsvUpperBounds)
    maskSmall = cv2.resize(mask, (int(frameSize[0] / 2), int(frameSize[1] / 2)))
    objectOfInterest = cv2.bitwise_and(frame, frame, mask=mask)
    objectOfInterestSmall = cv2.resize(objectOfInterest, (int(frameSize[0] / 2), int(frameSize[1] / 2)))
    cv2.putText(frame, str(int(fps)) + " FPS", overlayPosition, overlayFont, overlayFontScale, overlayFontColor, overlayFontThickness)
    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", maskSmall)
    cv2.imshow("Object", objectOfInterestSmall)
    if cv2.waitKey(1) == ord('q'):
        break
    frameElapsed = time() - frameStart
    updateFps(1 / frameElapsed, useLowPassFilter=True)
cv2.destroyAllWindows()
