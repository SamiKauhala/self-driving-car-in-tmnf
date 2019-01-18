""" test_data.py """

import os
import numpy as np
import cv2

def onehot_to_direction(key_choice, text):
    """Return a direction string."""
    for key, value in text.items():
        if any([i for i, key_choice in zip(key_choice, value) if i == key_choice]):
            return key

def main():
    """
    Display a collection of pictures and direction choices as a video.
    Check image and choice shapes.
    """
    image_desired_shape = (180, 240, 3)
    choice_desired_shape = (8,)
    compared_results = []
    total_num_frames = 0
    direction_text = {
        'Up + Left': [1, 0, 0, 0, 0, 0, 0, 0],
        'Up + Right': [0, 1, 0, 0, 0, 0, 0, 0],
        'Down + Left': [0, 0, 1, 0, 0, 0, 0, 0],
        'Down + Right': [0, 0, 0, 1, 0, 0, 0, 0],
        'Up': [0, 0, 0, 0, 1, 0, 0, 0],
        'Left': [0, 0, 0, 0, 0, 1, 0, 0],
        'Down': [0, 0, 0, 0, 0, 0, 1, 0],
        'Right': [0, 0, 0, 0, 0, 0, 0, 1]
    }

    # Config for text on images
    font = cv2.FONT_HERSHEY_SIMPLEX
    bot_left_c = (5, 175)
    font_scale = 0.4
    thickness = 1
    line_type = 8
    font_color = (25, 255, 25)

    for file in os.listdir('data'):
        print(f'Displaying: {file}')
        data = np.load(os.path.join('data', file))
        total_num_frames += len(data)

        for image, choice in data:
            choice = np.array(choice)

            if image.shape == image_desired_shape and choice.shape == choice_desired_shape:
                compared_results.append(1)
            else:
                compared_results.append(0)

            text = onehot_to_direction(choice, direction_text)

            cv2.putText(img=image,
                        text=text,
                        org=bot_left_c,
                        fontFace=font,
                        fontScale=font_scale,
                        color=font_color,
                        thickness=thickness,
                        lineType=line_type)

            cv2.imshow(f'Testing file {file}', cv2.resize(image, (384, 288)))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        cv2.destroyAllWindows()

    print(f'Total number of tested frames: {total_num_frames}')

    if min(compared_results) == 0:
        print('Data is not valid.')
    else:
        print('Data is valid.')

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
