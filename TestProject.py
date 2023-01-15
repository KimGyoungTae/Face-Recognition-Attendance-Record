import cv2
import numpy as np
import face_recognition
import os
import csv
import glob
from datetime import datetime

# from PIL import ImageGrab

cap = cv2.VideoCapture("http://192.168.35.193:8080/video")

imgElon = face_recognition.load_image_file('FaceFile/Elon Musk.jpg') #인코딩에 사용할 이미지 가져오기
encodeElon = face_recognition.face_encodings(imgElon)   #감지할 얼굴 인코딩, 첫번째 요소만 가져오기

imgKim = face_recognition.load_image_file('FaceFile/Kim Gyoung Tae.jpg') #인코딩에 사용할 이미지 가져오기
encodeKim = face_recognition.face_encodings(imgKim)  #감지할 얼굴 인코딩, 첫번째 요소만 가져오기

imgBaby = face_recognition.load_image_file('FaceFile/Baby Gyoung Tae.jpg') #인코딩에 사용할 이미지 가져오기
encodeBaby = face_recognition.face_encodings(imgBaby)   #감지할 얼굴 인코딩, 첫번째 요소만 가져오기

known_face_encoding = [
    encodeElon,
    encodeKim,
    encodeBaby
]

know_faces_names = [
  "Elon",
  "Kim Gyoung Tae",
  "Baby"
]

students = know_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date+'.csv','w+',newline= '')
lnwriter = csv.writer(f)

while True :
    _,frame = cap.read()
    imgS = cv2.resize(frame, (0, 0), fx= 0.25, fy= 0.25)
    rgb_frame = imgS[:,:,::-1]
    if s:
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings :
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = ""
            faceDis = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(faceDis)
            if matches[best_match_index]:
                name = know_faces_names[best_match_index]

            face_names.append(name)
            if name in know_faces_names:
                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name,current_time])

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == ord("q"):  # while 무한루프를 빠져나오기 위한 키보드 q를 눌러 WebCam 사용 중지
        break

cap.release()
cv2.destroyAllWindows()
f.close()

