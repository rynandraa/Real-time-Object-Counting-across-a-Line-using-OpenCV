import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import numpy as np
from time import sleep

# cap = cv2.VideoCapture('video.mp4')

largura_min = 80
altura_min = 80
offset = 6
pos_linha = 550

# FPS to vídeo
delay = 60

detec = []
carros = 0

	
def center_dot(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

class App:
    def __init__(self, window, window_title, video_source="video.mp4"):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
        self.delay = 15
        self.update()
        self.window.mainloop()
    
    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source="video.mp4"):
        subtracao = cv2.createBackgroundSubtractorMOG2()
    
        while True:
            ret, frame1 = video_source.read()
            tempo = float(1/delay)
            sleep(tempo) 
            grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(grey, (3, 3), 5)
            img_sub = subtracao.apply(blur)
            dilat = cv2.dilate(img_sub, np.ones((5, 5)))
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

            # The morphologyEx() of the method of the class Imgproc accepts src, dst, op, kernel as parameters
            dilatada = cv2.morphologyEx(dilat, cv2. MORPH_CLOSE, kernel)
            dilatada = cv2.morphologyEx(dilatada, cv2. MORPH_CLOSE, kernel)

            # OpenCV has findContour() function that helps in extracting the contours from the image.
            # It works best on binary images, so we should first apply thresholding techniques, Sobel edges, etc.
            contorno, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


            # it will create a line
            # Parameters:
            # image: It is the image on which line is to be drawn.
            # start_point: It is the starting coordinates of line.
            # end_point: It is the ending coordinates of line.
            # color: It is the color of line to be drawn.
            # thickness: It is the thickness of the line in px.
            cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (176, 130, 39), 2)
            for(i, c) in enumerate(contorno):
                (x, y, w, h) = cv2.boundingRect(c)
                validar_contorno = (w >= largura_min) and (h >= altura_min)
                if not validar_contorno:
                    continue

                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                centro = center_dot(x, y, w, h)
                detec.append(centro)
                cv2.circle(frame1, centro, 4, (0, 0, 255), -1)

                for (x, y) in detec:
                    if (y < (pos_linha + offset)) and (y > (pos_linha-offset)):
                        carros += 1
                        cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)
                        detec.remove((x, y))
                        print("No. of cars detected : " + str(carros))

            # cv2.putText() method is used to draw a text string on any image.
            # Parameters: image, text, org(coordinate), font, color, thickness
            cv2.putText(frame1, "VEHICLE COUNT : "+str(carros), (320, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 4)

    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
    
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    App(tkinter.Tk(), "Tkinter and OpenCV")
