import cv2
import numpy as np
import face_recognition
import os

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




#imgElon = face_recognition.load_image_file('faces/Elon Musk.jpg') #인코딩에 사용할 이미지 가져오기
#imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)  #RGB로 변환
#imgTest = face_recognition.load_image_file('faces/Face_image.jpg')  #Test 이미지 가져오기
#imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB) #Tset 이미지 RGB로 변환

