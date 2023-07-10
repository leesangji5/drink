from tensorflow import keras
import keras.utils as image
import numpy as np
import cv2
import gtts
import os
import playsound
import serial

# 아두이노 시리얼 모니터
# timeout 없으면 계속 기다려서 무한 루프에 빠짐
ser = serial.Serial('COM9', 9600, timeout=0.1)

# 모델 불러오기
model = keras.models.load_model('C:/drinkingDataSet/data/model/drink.h5')

# 카메라 실행 0번째 기본 카메라
cap = cv2.VideoCapture(0)

# tts text to speech
# text를 넣으면 text를 음성으로 변환하여 출력
def speak(text):
    # text를 음성으로 변환하여 저장
    tts = gtts.gTTS(text=text, lang='en')
    tts.save("C:/drinkingDataSet/data/audio/test.mp3")
    # 저장된 음성을 재생
    playsound.playsound("C:/drinkingDataSet/data/audio/test.mp3", True)
    # 저장된 음성을 삭제
    os.remove("C:/drinkingDataSet/data/audio/test.mp3")

# frame을 넣으면 frame을 예측하여 speak 함수를 실행
def predict(frame):
    # frame을 150, 150으로 resize
    img = cv2.resize(frame, (150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    # 예측
    y_pred = model.predict(img_tensor)

    # 예측 결과에 따라 speak 함수 실행
    if y_pred[0][0] > y_pred[0][1] and y_pred[0][0] > y_pred[0][2]:
        # 발음이 2pro로 하면 투pro 라고 해서 epro로 발음
        speak('epro')
        return '2pro'
    elif y_pred[0][1] > y_pred[0][0] and y_pred[0][1] > y_pred[0][2]:
        speak('cider')
        return 'cider'
    elif y_pred[0][2] > y_pred[0][0] and y_pred[0][2] > y_pred[0][1]:
        speak('coke')
        return 'coke'
    else :
        speak('i can not recognize')

# 음료 정보 출력
def speakDrinkInfo(drinkInfo, wantInfoList):
    if 0 in wantInfoList:
        speak(drinkInfo['name'])
    if 1 in wantInfoList:
        speak(drinkInfo['capacity'])
    if 2 in wantInfoList:
        speak(drinkInfo['calorie'])
    if 3 in wantInfoList:
        speak(drinkInfo['carbohydrate'])
    if 4 in wantInfoList:
        speak(drinkInfo['protein'])
    if 5 in wantInfoList:
        speak(drinkInfo['fat'])
    if 6 in wantInfoList:
        speak(drinkInfo['sodium'])
    if 7 in wantInfoList:
        speak(drinkInfo['sugar'])
    if 8 in wantInfoList:
        speak(drinkInfo['ingredient'])

# 음료이름 저장
drinkName = ''

# 음료 정보 1캔 기준 용량 구분 할 수 없음
# 2pro 이름, 용량, 칼로리, 탄수화물, 단백질, 지방, 나트륨, 당류, 재료
drink2pro = {
    'name': '2pro',
    'capacity': '240ml',
    'calorie': '65kcal',
    'carbohydrate': '16g',
    'protein': '0g',
    'fat': '0g',
    'sodium': '5mg',
    'sugar': '15g',
    'ingredient': 'Peach concentrate juice, purified water, high fructose liquid, synthetic flavoring, citric acid, trisodium citrate, enzyme treatment routine'
}
# cider 이름, 용량, 칼로리, 탄수화물, 단백질, 지방, 나트륨, 당류, 재료
drinkCider = {
    'name': 'cider',
    'capacity': '250ml',
    'calorie': '110kcal',
    'carbohydrate': '28g',
    'protein': '0g',
    'fat': '0g',
    'sodium': '5mg',
    'sugar': '27g',
    'ingredient': 'Purified water, high fructose corn syrup, white sugar, carbon dioxide, citric acid, lemon lime flavor'
}
# coke 이름, 용량, 칼로리, 탄수화물, 단백질, 지방, 나트륨, 당류, 재료
drinkCoke = {
    'name': 'coke',
    'capacity': '250ml',
    'calorie': '112kcal',
    'carbohydrate': '28g',
    'protein': '0g',
    'fat': '0g',
    'sodium': '15mg',
    'sugar': '27g',
    'ingredient': 'Purified water, sugar syrup, other fructose, sugar, carbon dioxide, caramel color, phosphoric acid, natural flavoring, caffeine'
}

while True:
    # cv2 기본 설정
    ret, frame = cap.read()
    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # 아두이노 값 읽기
    num = 0
    if ser.readable():
        # 보정 안한 값 = b'1\r\n'
        # b는 byte형식
        # \r\n기준으로 나누어서 [b'1', b'']으로 나뉨
        # b'1'만 가져옴
        # b'1'을 decode('utf-8')로 문자열로 변환
        # 보정 한 값 = 1
        a = ser.readline().split(b'\r\n')[0].decode('utf-8')
        if a != '':
            num = int(a)
    
    # 아두이노 값에 따라 실행
    if num == 1:
        # frame을 예측하여 음료 이름 저장
        drinkName = predict(frame)
        print(drinkName)
    elif num == 2:
        # 이름, 용량 출력
        if drinkName == '2pro':
            speakDrinkInfo(drink2pro, [0, 1])
        elif drinkName == 'cider':
            speakDrinkInfo(drinkCider, [0, 1])
        elif drinkName == 'coke':
            speakDrinkInfo(drinkCoke, [0, 1])
    elif num == 3:
        # 영양 정보 출력 (칼로리, 탄수화물, 단백질, 지방, 나트륨, 당류)
        if drinkName == '2pro':
            speakDrinkInfo(drink2pro, [2, 3, 4, 5, 6, 7])
        elif drinkName == 'cider':
            speakDrinkInfo(drinkCider, [2, 3, 4, 5, 6, 7])
        elif drinkName == 'coke':
            speakDrinkInfo(drinkCoke, [2, 3, 4, 5, 6, 7])
    elif num == 4:
        # 재료 출력
        if drinkName == '2pro':
            speakDrinkInfo(drink2pro, [8])
        elif drinkName == 'cider':
            speakDrinkInfo(drinkCider, [8])
        elif drinkName == 'coke':
            speakDrinkInfo(drinkCoke, [8])
    elif num == 5:
        pass
    elif num == 6:
        pass

# 카메라 종료
cap.release()
# cv2 종료
cv2.destroyAllWindows()
