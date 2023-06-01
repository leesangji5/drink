import tensorflow as tf
from tensorflow import keras
import keras.utils as image
import numpy as np
import cv2

model = keras.models.load_model('C:/drinkingDataSet/data/model/drink.h5')

cap = cv2.VideoCapture(0)

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

    if y_pred[0][0] > y_pred[0][1] and y_pred[0][0] > y_pred[0][2]:
        print('2pro')
    elif y_pred[0][1] > y_pred[0][0] and y_pred[0][1] > y_pred[0][2]:
        print('cider')
    elif y_pred[0][2] > y_pred[0][0] and y_pred[0][2] > y_pred[0][1]:
        print('coke')

cap.release()