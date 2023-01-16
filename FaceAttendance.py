import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime # 시간과 날짜에 대한 라이브러리
import json
import requests

#이미지 가져올 목록 생성
path = 'FaceFile'
images = []
classNames = []
myList = os.listdir(path) # 폴더의 이미지 목록을 가져오기 => os 라이브러리를 사용하여 많은 양의 이미지 저장가능
print(myList)#FaceFile 파일에 있는 이미지 목록 이름들이 출력됨.

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}') #이미지 읽기
    images.append(curImg) #현재 이미지 추가
    classNames.append(os.path.splitext(cl)[0]) #ex => Elon Musk.jpg 대신 Elon Musk로 분활
print(classNames)

##### 인코딩 계산하는 함수  #####
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  #RGB로 변환

        # encode = face_recognition.face_encodings(img)[0] # 감지할 얼굴 인코딩, 첫번째 요소만 가져오기
        encode = face_recognition.face_encodings(img)
        # 인코딩 했을 때 비어있는걸 (빈 배열) 가져와서 오류가 발생했었음.

        if not encode:
            print("입력 데이터 오류")
        else:
            encodeList.append(encode[0])  # 인코딩 찾은것을 목록에 추가
    return encodeList #목록들 반환


#### 출석 기록을 남기기 위한 함수 #####
def markAttendance(name: str):
    with open('./Attendance.csv', 'r+') as f:  # 동시에 읽고 쓰기를 원함.
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',') # ',' 기준으로 분할
            nameList.append(entry[0]) # 첫 번째 요소를 추가, entry[0]은 이름이 될 것이고, 목록의 이름만 추가하게 된다.
        if name not in nameList:    #이름 목록에 이름이 있는지 확인하기 위함.
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')     # 시/분/초
            current_date = now.strftime("%Y:%m:%d") # 년/월/일
            f.writelines(f'\n{name},{dtString},{current_date}')
            sendToMeMessage(text)  # 출석부에 기록 될 때 출석 알림 메세지 함수 호출!


####### 기존 오픈소스와 다르게 출석 확인을 알리기 위해 카카오톡 메세지를 보내준다. ######
def sendToMeMessage(text):
    header = {"Authorization": 'Bearer ' + "Access Token"}

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send" #나에게 보내기 주소

    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "출석 확인"
    }
    data = {"template_object": json.dumps(post)}
    return requests.post(url, headers=header, data=data)

#text = "Successful attendance.!!("+os.path.basename(__file__).replace(".py", ")")
text = "Face recognition attendance completed!!"
KAKAO_TOKEN = "TFS_000000000000000000000000000000000000000_sQ"
#print ((sendToMeMessage(text).text))


encodeListKnown = findEncodings(images)
print('Encoding Complete')


#### 기존 소스에서 노트북 카메라나 데스크탑 전용 카메라를 사용한 것을 스마트폰 카메라를 사용한 WebCam을 불러오게 소스 변환함! #####
cap = cv2.VideoCapture("Address of IP webcam") #IP webcam의 주소

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

import sys
while True:     #실시간으로 비디오 재생을 위해 while 반복문 사용

    success, img = cap.read() # 비디오가 있는지 없는지 bool 체크, 비디오 자체를 나타내는 img 변수
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)  # 픽셀크기는 정의하지 않고, 스케일을 0.25로 지정함.
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # RGB로 변환

    faceCurFrame = face_recognition.face_locations(imgS) # 이미지에서의 인코딩 위치 찾기
    encodesCurFrame = face_recognition.face_encodings(imgS,faceCurFrame) # 감지할 얼굴 인코딩, 프레임이 얼굴의 위치로 향하게

    for encodeFace,faceLoc in zip(encodesCurFrame,faceCurFrame): # 현재 프레임에서 인코딩된 얼굴과 프레임 상에서의 얼굴의 위치를 가져온다.
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace) #알려진 인코딩 목록과 현재 프레임에서 찾은 인코딩 된 얼굴과 비교하기
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis)
        # print(faceDis)
        # print(matchIndex)


        if matches[matchIndex]:
            name = classNames[matchIndex].upper() # 만약 3개의 이미지 자료가 있고, 웹켐에 보여지는 얼굴과 비교한 상황 => 3개의 이미지 자료 중 가장 낮은 수치가 얼굴과 가장 정확하다고 볼 수 있다.
            # upper()은 가장 정확한 이미지 이름을 소문자로 되어있다면 대문자로 변환하여 출력시켜준다.
            print(f"Prediction Face: {name}")
            #
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 웹켐 상에서 보여지는 얼굴에 네모난 직사각형이 그려짐.
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)   # 직사각형으로 가리키고 있는 얼굴이 무엇인지 화면에 표시해줌.
            markAttendance(name) # 출석 기록 함수 호출


    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord("q"): #while 무한루프를 빠져나오기 위한 키보드 q를 눌러 WebCam 사용 중지
        break

cap.release()
cv2.destroyAllWindows()
