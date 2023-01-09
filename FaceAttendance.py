import cv2
import numpy as np
import face_recognition
import os

from datetime import datetime


#이미지 가져올 목록 생성
path = 'faces'
images = []
classNames = []
myList = os.listdir(path)#폴더의 이미지 목록을 가져오기
print(myList)#faces 파일에 있는 이미지 목록 이름들이 출력됨.

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}') #이미지 읽기
    images.append(curImg)#현재 이미지 추가
    classNames.append(os.path.splitext(cl)[0]) #ex => Elon Musk.jpg 대신 Elon Musk로 분활
print(classNames)

#인코딩 계산하는 함수
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  #RGB로 변환
        encode = face_recognition.face_encodings(img)[0]  # 감지할 얼굴 인코딩, 첫번째 요소만 가져오기
        encodeList.append(encode) #인코딩 찾은것을 목록에 추가
    return encodeList #목록들 반환

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

encodeListKnown = findEncodings(images)
print('Encoding Complete')


cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # RGB로 변환

    faceCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,faceCurFrame) # 감지할 얼굴 인코딩, 첫번째 요소만 가져오기

    for encodeFace,faceLoc in zip(encodesCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace) #알려진 인코딩 목록과 인코딩 된 얼굴과 비교하기
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)

        cv2.imshow('Webcam', img)
        cv2.waitKey(1)

''''
#얼굴의 위치 같게 만들기
faceLoc = face_recognition.face_locations(imgElon)[0]
encodeElon = face_recognition.face_encodings(imgElon)[0]   #감지할 얼굴 인코딩, 첫번째 요소만 가져오기
cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]), (faceLoc[1],faceLoc[2]),(255,0,255),2) #우리가 얼굴을 감지한 위치를 확인하기 위해 사각형을 이미지에 그림

faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]   #Test이미지에 대한 첫번째 요소만 가져오기
cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]), (faceLocTest[1],faceLocTest[2]),(255,0,255),2) #Test 이미지에 사각형 이미지

results = face_recognition.compare_faces([encodeElon],encodeTest) #인코딩 이미지와 Test 이미지 간의 비교하기
faceDis = face_recognition.face_distance([encodeElon],encodeTest) #이미지 유사성 알기, (==> 얼굴 간의 오차 느낌인거 같음)
'''''
