#Помогаев Максим 2 Вариант

import cv2
import time

# 1
def image_processing(): 
  src = cv2.imread('images/variant-2.png')
  scale_percent = 50
  width = int(src.shape[1] * scale_percent / 100)
  height = int(src.shape[0] * scale_percent / 100)

  output = cv2.resize(src, (width,height))

  output_gauss = cv2.GaussianBlur(output, (5, 5), 0)

  cv2.imshow('image', output_gauss)

# 2,3 addition
def video_processing():
    cap = cv2.VideoCapture(0)
    down_points = (640, 480)
    file = open('coordinates.txt', 'w')
    coordinates = []
    i = 0
    src = cv2.imread('fly64.png')
    src = cv2.resize(src, (32, 32))
    src_height, src_width, _ = src.shape
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            x_center = x + ((w // 2) - 16)
            y_center = y + ((h // 2) - 16)
            frame[y_center:y_center + src_height, x_center:x_center + src_width] = src

            if i % 5 == 0:
                a = x + (w // 2)
                b = y + (h // 2)
                coordinates.append(a)
                coordinates.append(b)
                print(a, b)
                file.write(str(coordinates) + '\n')
                coordinates.clear()

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)
        i += 1

    cap.release()


if __name__ == '__main__':
    image_processing()
    video_processing()

cv2.waitKey(0)
cv2.destroyAllWindows()