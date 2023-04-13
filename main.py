#library
import cv2
import numpy as np
from time import sleep

#
width_min = 80
height_min = 80
#ambang batas garis dengan mobil lewat
offset = 6
#tempat dimana garis diposisi kan
pos_line = 550
 
# FPS to vídeo
delay = 60
#objek yang terdeteksi
detec = []
#variabel car untuk mendeteksi/menghitung mobil bergerak
car = 0

#fungsi untuk mendeteksi center atau titik tengah dari objk
def center_dot(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


# video source input
# kita dapat memilih untuk menggunakan video yang disediakan atau menggunakan webcam
cap = cv2.VideoCapture('video.mp4')
# OpenCV menyediakan algoritma Background Subtraction.
# kita dapat melakukan Pengurangan latar belakang menggunakan pengurangan matriks, yaitu, hanya mengurangi bingkai statis dari video.

#untuk melihat perubahan background
subtraction = cv2.createBackgroundSubtractorMOG2()

#untuk membuka file inputan dan memprosesnya
while True:
    ret, frame1 = cap.read()
    #untuk delay yang dilakukan
    tempo = float(1/delay)
    sleep(tempo) 
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = subtraction.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # The morphologyEx() of the method of the class Imgproc accepts src, dst, op, kernel as parameters
    dilatada = cv2.morphologyEx(dilat, cv2. MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2. MORPH_CLOSE, kernel)

    contour, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    # it will create a line
    # Parameters:
    # gambar: Ini adalah gambar di mana garis akan ditarik.
    # start_point: Ini adalah koordinat awal garis.
    # end_point: Ini adalah koordinat akhir garis.
    # warna: Ini adalah warna garis yang akan digambar.
    # ketebalan: Ini adalah ketebalan garis dalam px.
    # mendeteksi contour
    # jika ingin menyesuaikan garis kita dapat mengubah nilai nilai dari fungsi berikut
    cv2.line(frame1, (25, pos_line), (1200, pos_line), (0, 0, 255), 2)
    for(i, c) in enumerate(contour):
        (x, y, w, h) = cv2.boundingRect(c)
        validar_contour = (w >= width_min) and (h >= height_min)
        if not validar_contour:
            continue
        
        #bounding box dari frame1
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #mencari titik tengah dari objek
        center = center_dot(x, y, w, h)
        detec.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)

        #setiap box dari objek dideteksi apakah menyentuh atau melewati garis
        for (x, y) in detec:
            if (y < (pos_line + offset)) and (y > (pos_line-offset)):
                car += 1
                cv2.line(frame1, (25, pos_line), (1200, pos_line), (176, 130, 39), 3)
                detec.remove((x, y))
                print("No. of cars detected : " + str(car))

    # Parameters: image, text, org(coordinate), font, color, thickness
    cv2.putText(frame1, "VEHICLE COUNT : "+str(car), (320, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 127, 255), 4)
    cv2.imshow("Video Original", frame1)
    cv2.imshow(" Detector ", dilatada)

    # To display the image, you can use the imshow() method of cv2
    if cv2.waitKey(1) == 27:
        break
    
cv2.destroyAllWindows()
cap.release()
