""" collect_data.py """

import os
import time
import threading
import pynput
from mss import mss
import numpy as np
import cv2

class StopCollecting(Exception):
    pass

def get_filename(dirname):
    """Return the path and name for new savefile."""
    try:
        if os.path.isdir(dirname):
            num_files = len(os.listdir(dirname))

        if os.path.isfile(f'{dirname}/TRAINING_DATA-{(num_files + 1)}.npy'):
            num_files += 1

        file_name = f'TRAINING_DATA-{(num_files + 1)}.npy'
        path_to_file = os.path.join(dirname, file_name)
        print(f'Filename: {path_to_file}')

    except NotADirectoryError:
        print('Not a valid directory name!')

    return path_to_file

def take_screen(resize_dimensions):
    """Return a screenshot with resized dimensions."""
    captured_area = {'top': 24,
                     'left': 4,
                     'width': 640,
                     'height': 480}

    with mss() as sct:

        image = np.array(sct.grab(captured_area))
        image = cv2.resize(image, resize_dimensions)
        # Remove alpha channel from the captured image.
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        return image

def on_press(key):
    """Save image and key output to list and append to TRAINING_DATA."""
    keys_to_listen_for = {pynput.keyboard.Key.up, pynput.keyboard.Key.left,
                          pynput.keyboard.Key.down, pynput.keyboard.Key.right}

    combinations = [{pynput.keyboard.Key.up, pynput.keyboard.Key.left},
                    {pynput.keyboard.Key.up, pynput.keyboard.Key.right},
                    {pynput.keyboard.Key.down, pynput.keyboard.Key.left},
                    {pynput.keyboard.Key.down, pynput.keyboard.Key.right}]

    output = []

    if key == pynput.keyboard.KeyCode(char='p'):
        raise StopCollecting

    if key in keys_to_listen_for:
        CURRENT_KEYS.add(key)
        if all(k in CURRENT_KEYS for k in combinations[0]):
            output = [1, 0, 0, 0, 0, 0, 0, 0]
        elif all(k in CURRENT_KEYS for k in combinations[1]):
            output = [0, 1, 0, 0, 0, 0, 0, 0]
        elif all(k in CURRENT_KEYS for k in combinations[2]):
            output = [0, 0, 1, 0, 0, 0, 0, 0]
        elif all(k in CURRENT_KEYS for k in combinations[3]):
            output = [0, 0, 0, 1, 0, 0, 0, 0]
        elif key == pynput.keyboard.Key.up:
            output = [0, 0, 0, 0, 1, 0, 0, 0]
        elif key == pynput.keyboard.Key.left:
            output = [0, 0, 0, 0, 0, 1, 0, 0]
        elif key == pynput.keyboard.Key.down:
            output = [0, 0, 0, 0, 0, 0, 1, 0]
        elif key == pynput.keyboard.Key.right:
            output = [0, 0, 0, 0, 0, 0, 0, 1]

    if output:
        image = take_screen(resize_dimensions=(240, 180))
        TRAINING_DATA.append([image, output])

def print_datalen(data):
    """Print lenght of input data every 60 seconds."""
    while True:
        if data:
            print(f'Number of training data frames: {len(data)}')
            time.sleep(60)

def on_release(key):
    """Remove last key that was added to CURRENT_KEYS."""
    try:
        CURRENT_KEYS.remove(key)

    except KeyError:
        pass

def main():
    """Listen to keyboard input, take screenshots and save them to a .npy datastructure on exit."""
    print('Starting data collection... ')
    for i in list(range(5))[::-1]:
        print(str(i + 1))
        time.sleep(1)

    file_name = get_filename('data')
    datalen_thread = threading.Thread(target=print_datalen, args=(TRAINING_DATA,))
    datalen_thread.daemon = True
    datalen_thread.start()

    while True:
        with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            try:
                listener.join()

            except StopCollecting:
                break

    print(f'Saving {len(TRAINING_DATA)} frames of data.')
    np.save(file_name, TRAINING_DATA)
    print('Exiting...')

if __name__ == '__main__':
    CURRENT_KEYS = set()
    TRAINING_DATA = []
    main()
