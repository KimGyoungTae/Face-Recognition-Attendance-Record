# [OSSP] Face-recognition Attendance record project
동계 계절학기 오픈소스 프로젝트 : 얼굴 인식 출석 기록 프로젝트

⭐ 기존 오픈소스를 분석하고, 기존 프로젝트의 문제점을 찾아 개선점을 추가하는 것이 이번 과목의 핵심이다.
<br>
⭐ 출석 기록 확인을 엑셀 파일에서만이 아닌 카카오톡 알림으로 출석 확인을 실시간으로 가능하게 기능을 추가. 


## 🖥️ 프로젝트 소개
OpenCV를 활용하여 사용자의 얼굴을 인식하여 일치할 시 출석부에 기록을 남기면서 동시에 카카오톡으로 출석 확인 메시지가 전달됩니다.
![image](https://user-images.githubusercontent.com/83820089/218441603-4243ab43-5ea0-41ce-a9f4-1ae1947103ce.png)

### 🤝 기존 오픈소스 : https://github.com/murtazahassan/Face-Recognition
<br>

## 🕰️ 개발 기간
* 23.01.05일 - 23.01.17일

### ⚙️ 개발 환경
- `PyCharm`

### 📝 개발 정리 : https://vrworld.tistory.com/
<br>

## 📌 주요 기능
- WebCam 을 이용하여 모바일 환경에서도 실시간 얼굴인식 진행
- 얼굴인식 성공 시 얼굴 위치에 출석을 확인받은 사람의 이름을 보여준다.
- 출석이 정상적으로 처리된 사람들의 출석명부를 엑셀 파일에 현재 날짜, 시간을 기록한다.
- 카카오 REST API를 이용하여 출석이 처리된 동시에 카카오톡으로 출석 확인 메시지가 전송된다.


![image](https://user-images.githubusercontent.com/83820089/218441416-ce6326a4-cab3-41bf-86ab-5e1f32faa7fa.png)

![image](https://user-images.githubusercontent.com/83820089/218441823-692421d7-43b7-483b-b791-2c687a5f08b4.png)


