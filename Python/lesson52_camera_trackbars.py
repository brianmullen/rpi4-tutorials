import cv2
from picamera2 import Picamera2
from time import time
from _Rect import Rect

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

rectangle = Rect(0, 0, 100, 100)
rectangleColor=(0, 255, 0)
rectangleThickness=1                                    # -1 for solid

def onXChange(newValue):
    global rectangle, frameSize
    
    if newValue + rectangle.width >= frameSize[0] - 1:
        rectangle.x = frameSize[0] - 1 - rectangle.width
    else:
        rectangle.x = newValue

def onYChange(newValue):
    global rectangle, frameSize
    
    if newValue + rectangle.height >= frameSize[1] - 1:
        rectangle.y = frameSize[1] - 1 - rectangle.height
    else:
        rectangle.y = newValue

def onWidthChange(newValue):
    global rectangle, frameSize
    
    if rectangle.x + newValue >= frameSize[0] - 1:
        rectangle.width = frameSize[0] - 1 - rectangle.x
    else:
        rectangle.width = newValue

def onHeightChange(newValue):
    global rectangle, frameSize
    
    if rectangle.y + newValue >= frameSize[1] - 1:
        rectangle.height = frameSize[1] - 1 - rectangle.y
    else:
        rectangle.height = newValue

cv2.namedWindow('Trackbars')
cv2.createTrackbar('X:', 'Trackbars', 10, frameSize[0] - 1, onXChange)
cv2.createTrackbar('Y:', 'Trackbars', 10, frameSize[1] - 1, onYChange)
cv2.createTrackbar('Width:', 'Trackbars', 10, frameSize[0] - 1, onWidthChange)
cv2.createTrackbar('Height:', 'Trackbars', 10, frameSize[1] - 1, onHeightChange)

def updateFps(newValue: float, useLowPassFilter: bool = True):
    global fps

    if useLowPassFilter:
        fps = 0.9 * fps + 0.1 * newValue
    else:
        fps = newValue

while True:
    frameStart = time()
    frame = camera.capture_array()
    region = frame[rectangle.y: rectangle.y + rectangle.height, rectangle.x: rectangle.x + rectangle.width]

    cv2.putText(frame, str(int(fps)) + " FPS", overlayPosition, overlayFont, overlayFontScale, overlayFontColor, overlayFontThickness)
    cv2.rectangle(frame, (rectangle.x, rectangle.y), (rectangle.x + rectangle.width, rectangle.y + rectangle.height), rectangleColor, rectangleThickness)

    cv2.imshow("Camera", frame)
    cv2.imshow("Region", region)
    if cv2.waitKey(1) == ord('q'):
        break
    frameElapsed = time() - frameStart
    updateFps(1 / frameElapsed, useLowPassFilter=True)
cv2.destroyAllWindows()
