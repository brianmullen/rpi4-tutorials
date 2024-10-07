import cv2
from picamera2 import Picamera2
from time import time

from traitlets import Bool

fps = 58.92
frameWidth=640
frameHeight=480
camera=Picamera2()
# print(camera.sensor_modes)
camera.preview_configuration.main.size=(frameWidth, frameHeight)
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

rectangleX = 0
rectangleY = 0
rectangleWidth=100
rectangleHeight=50
rectangleColor=(0, 255, 0)
rectangleThickness=-1                                    # -1 for solid

movementSpeed=60.0
horizontalDirection = 1
verticalDirection = 1

def updateFps(newValue: float, useLowPassFilter: Bool = True):
    global fps

    if useLowPassFilter:
        fps = 0.9 * fps + 0.1 * newValue
    else:
        fps = newValue

while True:
    frameStart = time()
    frame = camera.capture_array()
    cv2.putText(frame, str(int(fps)) + " FPS", overlayPosition, overlayFont, overlayFontScale, overlayFontColor, overlayFontThickness)

    rectangleX += movementSpeed * horizontalDirection / fps
    if rectangleX + rectangleWidth >= (frameWidth - 1):
        rectangleX = frameWidth - 1 - rectangleWidth
        horizontalDirection *= -1
    elif rectangleX <= 0:
        rectangleX = 0
        horizontalDirection *= -1
    rectangleY += movementSpeed * verticalDirection / fps
    if rectangleY + rectangleHeight >= (frameHeight - 1):
        rectangleY = frameHeight - 1 - rectangleHeight
        verticalDirection *= -1
    elif rectangleY <= 0:
        rectangleY = 0
        verticalDirection *= -1

    rectangleUpperLeft=(int(rectangleX), int(rectangleY))
    rectangleLowerRight=(int(rectangleX) + rectangleWidth, int(rectangleY) + rectangleHeight)
    cv2.rectangle(frame, rectangleUpperLeft, rectangleLowerRight, rectangleColor, rectangleThickness)

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break
    frameElapsed = time() - frameStart
    updateFps(1 / frameElapsed, useLowPassFilter=True)
cv2.destroyAllWindows()
