import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime # 시간과 날짜에 대한 라이브러리

#이미지 가져올 목록 생성
path = 'faces'
images = []
classNames = []
myList = os.listdir(path)#폴더의 이미지 목록을 가져오기
print(myList)#faces 파일에 있는 이미지 목록 이름들이 출력됨.

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}') #이미지 읽기
    images.append(curImg) #현재 이미지 추가
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
    with open('Attendance.csv','r+') as f:  # 동시에 읽고 쓰기를 원함.
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',') # ',' 기준으로 분할
            nameList.append(entry[0]) # 첫 번째 요소를 추가, entry[0]은 이름이 될 것이고, 목록의 이름만 추가하게 된다.
        if name not in nameList:    #이름 목록에 이름이 있는지 확인하기 위함.
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

encodeListKnown = findEncodings(images)
print('Encoding Complete')


# 기존 노트북 카메라나 데스크탑 전용 카메라를 사용한 것을 스마트폰 카메라를 사용해서 WebCam을 불러오게 소스 변환
cap = cv2.VideoCapture("http://192.168.35.193:8080/video") #IP webcam의 주소

while True:     #실시간으로 비디오 재생을 위해 while 반복문 사용
    success, img = cap.read() # 비디오가 있는지 없는지 bool 체크, 비디오 자체를 나타내는 img 변수
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)  # 픽셀크기는 정의하지 않고, 스케일을 0.25로 지정함.
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # RGB로 변환

    faceCurFrame = face_recognition.face_locations(imgS) # 이미지에서의 인코딩 위치 찾기
    encodesCurFrame = face_recognition.face_encodings(imgS,faceCurFrame) # 감지할 얼굴 인코딩, 프레임이 얼굴의 위치로 향하게

    for encodeFace,faceLoc in zip(encodesCurFrame,faceCurFrame): # 현재 프레임에서 인코딩된 얼굴과 프레임 상에서의 얼굴의 위치를 가져온다.
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace) #알려진 인코딩 목록과 현재 프레임에서 찾은 인코딩 된 얼굴과 비교하기
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDis)  # 상대적으로 가장 낮은게 가장 일치하다고 볼 수 있다.
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper() # 만약 3개의 이미지 자료가 있고, 웹켐에 보여지는 얼굴과 비교한 상황 => 3개의 이미지 자료 중 가장 낮은 수치가 얼굴과 가장 정확하다고 볼 수 있다.
            # upper()은 가장 정확한 이미지 이름을 소문자로 되어있다면 대문자로 변환하여 출력시켜준다.
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 웹켐 상에서 보여지는 얼굴에 네모난 직사각형이 그려짐.
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)   # 직사각형으로 가리키고 있는 얼굴이 무엇인지 화면에 표시해줌.
            markAttendance(name) # 얼굴을 찾을 때마다 함수 호출

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord("q"): #while 무한루프를 빠져나오기 위한 키보드 q를 눌러 WebCam 사용 중지
        break 

cap.release()
cv2.destroyAllWindows()

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
