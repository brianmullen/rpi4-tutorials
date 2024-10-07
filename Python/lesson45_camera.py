import cv2
import picamera2

camera=picamera2.Picamera2()
camera.preview_configuration.main.size=(1280,720)
camera.preview_configuration.main.format="RGB888"
camera.preview_configuration.align()    # Picks closest standard size to specified size
camera.configure("preview")
camera.start()

while True:
    frame = camera.capture_array()
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
