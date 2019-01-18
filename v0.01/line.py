import numpy as np
import cv2

class Line:
    def __init__(self, x1, y1, x2, y2):
        
        self.x1 = np.float32(x1)
        self.y1 = np.float32(y1)
        self.x2 = np.float32(x2)
        self.y2 = np.float32(y2)
        
        self.slope = self.get_slope()
        self.bias = self.get_bias()
        self.distance = self.get_distance()
        
    def get_slope(self):
        return (self.y2 - self.y1) / (self.x2 - self.x1 + np.finfo(float).eps)
    
    def get_bias(self):
        return self.y1 - self.slope * self.x1

    def get_coords(self):
        return np.array([self.x1, self.y1, self.x2, self.y2])

    def draw(self, img, color=[255, 25, 25], thickness=10):
        cv2.line(img, (self.x1, self.y1), (self.x2, self.y2), color, thickness)
        
    def get_distance(self):
        return np.sqrt(np.square(self.y2 - self.y1) + np.square(self.x2 - self.x1))