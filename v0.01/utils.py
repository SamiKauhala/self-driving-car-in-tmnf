import numpy as np
import cv2
from line import Line

def numpy_flip(img):
    frame = np.array(img, dtype=np.uint8)
    return np.flip(frame[:, :, :3], 2)

def extract_channels(img, channel):
    return img[:, :, channel]

def threshold(img, thresh_min, thresh_max):
    output = np.zeros_like(img)
    output[(img >= thresh_min) & (img <= thresh_max)] = 1
    return (output * 255) 

def roi(img, vertices):
    mask = np.zeros_like(img)  
    cv2.fillPoly(mask, vertices, 255)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    return lines

def weighted_img(img, initial_img, alpha=0.8, beta=1., gamma=0.):
    return cv2.addWeighted(initial_img, alpha, img, beta, gamma)

def process_image(img, roi_vertices):
    
    original_img = img.copy()
    
    processed_img = extract_channels(img, 0)
    
    processed_img = threshold(processed_img, 100, 230)
    
    gx = cv2.Sobel(processed_img, cv2.CV_16S, 1, 0, 3)
    gy = cv2.Sobel(processed_img, cv2.CV_16S, 0, 1, 3)
    
    abs_x = cv2.convertScaleAbs(gx)
    abs_y = cv2.convertScaleAbs(gy)
    
    processed_img = weighted_img(abs_x, abs_y)
    
    processed_img = roi(processed_img, roi_vertices)
    
    lines = hough_lines(processed_img, 3, np.pi/180, 100, 100, 15)
        
    lines = [Line(l[0][0], l[0][1], l[0][2], l[0][3]) for l in lines]
    
    lanes = find_lane(original_img, lines)
    
    if len(lanes) > 0:
        line_image = np.zeros_like(original_img)
        
        for lane in lanes:
            lane.draw(line_image)
        
        weighted = weighted_img(line_image, original_img)
    
        return processed_img, weighted
    else:
        return processed_img, original_img
    
def find_lane(img, lines):
                  
    x_size = img.shape[1]
    y_size = img.shape[0]
    lines_slope_bias = np.zeros(shape=(len(lines),2))
    
    for index,line in enumerate(lines):        
        slope = line.slope
        bias = line.bias
        lines_slope_bias[index]=[slope, bias]
            
    max_slope_line = lines_slope_bias[lines_slope_bias.argmax(axis=0)[0]]
    min_slope_line = lines_slope_bias[lines_slope_bias.argmin(axis=0)[0]]
    
    left_slopes = []
    left_biases = []
    right_slopes = []
    right_biases = []
    
    for line in lines_slope_bias:
        if abs(line[0] - max_slope_line[0]) < 0.15 and abs(line[1] - max_slope_line[1]) < (0.15 * x_size):
            left_slopes.append(line[0])
            left_biases.append(line[1])
        elif abs(line[0] - min_slope_line[0]) < 0.15 and abs(line[1] - min_slope_line[1]) < (0.15 * x_size):
            right_slopes.append(line[0])
            right_biases.append(line[1])
              
    new_lines = np.zeros(shape=(1,2,4), dtype=np.int32)
    if len(left_slopes) > 0:
        left_line = [np.mean(left_slopes), np.mean(left_biases)]
        left_bottom_x = (y_size - left_line[1]) / left_line[0]
        left_top_x = (y_size * 0.575 - left_line[1]) / left_line[0]
        if (left_bottom_x >= 0):
            new_lines[0][0] =[left_bottom_x,y_size,left_top_x,y_size * 0.575]
    if len(right_slopes) > 0:
        right_line = [np.mean(right_slopes), np.mean(right_biases)]
        right_bottom_x = (y_size - right_line[1]) / right_line[0]
        right_top_x = (y_size * 0.575 - right_line[1]) / right_line[0]
        if (right_bottom_x <= x_size):
            new_lines[0][1]=[right_bottom_x,y_size,right_top_x,y_size * 0.575]
     
    left_l = Line(new_lines[0][0][0], 
                  new_lines[0][0][1], 
                  new_lines[0][0][2], 
                  new_lines[0][0][3])
    
    right_l = Line(new_lines[0][1][0], 
                   new_lines[0][1][1], 
                   new_lines[0][1][2], 
                   new_lines[0][1][3])
    
    return left_l, right_l
