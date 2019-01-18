""" test_model.py """

import os
import time
import numpy as np
import cv2
import pynput
from mss import mss
from models import inceptionv3
from keys import forward, left, reverse, right, \
forward_left, forward_right, reverse_left, \
reverse_right

def main():
    image_width = 240
    image_height = 180
    learning_rate = 1e-3
    epochs = 25
    datalen = 100
    model_type = 'inceptionv3'
    model_name = f'tmnf-car-{learning_rate}-{model_type}-{epochs}-epochs-{datalen}K-data.model'

    model = inceptionv3(image_width, image_height, 3, learning_rate, output=8, model_name=model_name)
    model.load(os.path.join('models', model_name))

    captured_area = {'top': 0,
                     'left': 0,
                     'width': 1920,
                     'height': 1080}

    controller = pynput.keyboard.Controller()

    print('Starting in... ')
    for i in list(range(5))[::-1]:
        print((i + 1))
        time.sleep(1)

    with mss() as sct:
        while True:
            time_before_prediction = time.time()

            image = np.array(sct.grab(captured_area))
            image = cv2.resize(image, (image_width, image_height))
            # Remove alpha channel from captured image.
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

            prediction = model.predict(image.reshape(-1, image_width, image_height, 3))[0]
            prediction = (np.array(prediction) * np.array([1.1, 1.1, 0.5, 0.5, 6, 0.1, 0.1, 0.1]))
            direction_choice = np.argmax(prediction)

            if direction_choice == 0:
                forward_left(controller)
                choice_picked = 'Forward + Left'

            elif direction_choice == 1:
                forward_right(controller)
                choice_picked = 'Forward + Right'

            elif direction_choice == 2:
                reverse_left(controller)
                choice_picked = 'Reverse + Left'

            elif direction_choice == 3:
                reverse_right(controller)
                choice_picked = 'Reverse + Right'

            elif direction_choice == 4:
                forward(controller)
                choice_picked = 'Forward'

            elif direction_choice == 5:
                left(controller)
                choice_picked = 'Left'

            elif direction_choice == 6:
                reverse(controller)
                choice_picked = 'Reverse'

            elif direction_choice == 7:
                right(controller)
                choice_picked = 'Right'

            print(f'Prediction took: {round(time.time() - time_before_prediction, 3)} s\
             / Direction: {choice_picked}')

if __name__ == '__main__':
    main()
