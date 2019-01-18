import numpy as np
import cv2
from mss import mss
from utils import process_image, numpy_flip
import time

def main():
    monitor = {'top': 25,
                'left': 700,
                'width': 1920,
                'height': 875}

    roi_vertices = np.expand_dims(np.array([
            [0, 435],
            [0, 190],
            [320, 175],
            [638, 190],
            [638, 435],
            [435, 435],
            [355, 275],
            [283, 275],
            [203, 435]
        ], np.int32), axis=0)
    
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)
    
    with mss() as sct:   
        while(True):
            image = np.array(sct.grab(monitor))
            
            try:
                new_img = numpy_flip(image)
                
                processed_image, original_img = process_image(new_img, roi_vertices)
                
                #cv2.imshow('Lanes', processed_image)
                cv2.imshow('Lanes', cv2.resize(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB), (600, 500)))
                
            except Exception as e:
                print(str(e))
                pass
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':
    main()