import cv2
import time

def take_photos(qty):
    cap = cv2.VideoCapture(0)

    for i in range(qty):
        frame = cap.read()[1]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img_path = f"captured/{i}.png"
        cv2.imwrite(img_path, gray)
        time.sleep(1.0)

    cap.release()
    cv2.destroyAllWindows()

#take_photos(5)