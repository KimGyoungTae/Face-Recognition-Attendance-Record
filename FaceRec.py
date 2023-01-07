import cv2
import numpy as np
import face_recognition

imgElon = face_recognition.load_image_file('faces/Elon Musk.jpg') #인코딩에 사용할 이미지 가져오기
imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)  #RGB로 변환
imgTest = face_recognition.load_image_file('faces/Face_image.jpg')  #Test 이미지 가져오기
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB) #Tset 이미지 RGB로 변환

#얼굴의 위치 같게 만들기
faceLoc = face_recognition.face_locations(imgElon)[0]
encodeElon = face_recognition.face_encodings(imgElon)[0]   #감지할 얼굴 인코딩, 첫번째 요소만 가져오기
cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]), (faceLoc[1],faceLoc[2]),(255,0,255),2) #우리가 얼굴을 감지한 위치를 확인하기 위해 사각형을 이미지에 그림

faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]   #Test이미지에 대한 첫번째 요소만 가져오기
cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]), (faceLocTest[1],faceLocTest[2]),(255,0,255),2) #Test 이미지에 사각형 이미지

results = face_recognition.compare_faces([encodeElon],encodeTest) #인코딩 이미지와 Test 이미지 간의 비교하기
faceDis = face_recognition.face_distance([encodeElon],encodeTest) #이미지 유사성 알기, (==> 얼굴 간의 오차 느낌인거 같음)
print(results, faceDis) #두 개의 이미지가 서로 같으면 True, 다른 이미지일 경우 False를 출력한다

#이미지에 대한 결과랑 유사성을 Test 이미지에 명시해주기, round()는 유사성을 소수점 둘째짜리로 반올림 한다는 뜻
cv2.putText(imgTest, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

cv2.imshow('Elon Musk',imgElon) #인코딩 이미지 불러오기
cv2.imshow('Face_image',imgTest) #Test 이미지 불러오기
cv2.waitKey(0)






