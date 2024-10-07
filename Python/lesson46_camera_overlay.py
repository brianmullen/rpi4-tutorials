import cv2
from picamera2 import Picamera2
from time import time

from traitlets import Bool

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
overlayFontColor = (0, 0, 255)                          # opencv uses GBR colorspace
overlayFontThickness = 3

def updateFps(newValue: float, useLowPassFilter: Bool = True):
    global fps

    if useLowPassFilter:
        fps = 0.9 * fps + 0.1 * newValue
    else:
        fps = newValue

while True:
    frameStart = time()
    frame = camera.capture_array()
    cv2.putText(frame, str(int(fps)), overlayPosition, overlayFont, overlayFontScale, overlayFontColor, overlayFontThickness)
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break
    frameElapsed = time() - frameStart
    updateFps(1 / frameElapsed, useLowPassFilter=True)
cv2.destroyAllWindows()
