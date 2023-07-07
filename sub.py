from tensorflow import keras
import keras.utils as image
import numpy as np
import cv2
import gtts
import os
import playsound
import time

def speak(text):
    tts = gtts.gTTS(text=text, lang='en')
    tts.save("C:/drinkingDataSet/data/audio/test.mp3")
    playsound.playsound("C:/drinkingDataSet/data/audio/test.mp3", True)
    os.remove("C:/drinkingDataSet/data/audio/test.mp3")

def predict():
    y_pred = model.predict(img_tensor)

    if y_pred[0][0] > y_pred[0][1] and y_pred[0][0] > y_pred[0][2]:
        speak('epro')
    elif y_pred[0][1] > y_pred[0][0] and y_pred[0][1] > y_pred[0][2]:
        speak('cider')
    elif y_pred[0][2] > y_pred[0][0] and y_pred[0][2] > y_pred[0][1]:
        speak('coke')

model = keras.models.load_model('C:/drinkingDataSet/data/model/drink.h5')
cap = cv2.VideoCapture(0)
st = time.time()

while True:
    ret, frame = cap.read()
    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    img = cv2.resize(frame, (150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    y_pred = model.predict(img_tensor)

    if time.time() - st > 3:
        predict()
        st = time.time()

cap.release()
cv2.destroyAllWindows()