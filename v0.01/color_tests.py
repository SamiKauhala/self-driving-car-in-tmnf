import numpy as np
import cv2

'''
Test Images
    img.jpg
    img1.jpg
    img2.jpg
    img3.jpg
    img4.jpg
    img5.jpg

Color Channels
    RGB -> R; best
    HSV -> S    
    HLS -> S
    LAB -> L
    LUV -> L
'''

image = cv2.imread('img5.jpg', 1)

src = np.array([[-300, 300], [260, 210], [380, 210], [940, 300]], np.float32)

dst = np.array([[180, 480], [180, 0], [420, 0], [420, 480]], np.float32)

M = cv2.getPerspectiveTransform(src, dst)
image_size = (image.shape[1], image.shape[0])

warped_image = cv2.warpPerspective(image, M, dsize=image_size)

channel = warped_image[:, :, 0]
thresh = (100, 230)
output = np.zeros_like(channel)
output[(channel >= thresh[0]) & (channel <= thresh[1])] = 1
