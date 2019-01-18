# keys.py

import time
import pynput

def forward(controller, press_duration = 0.0075):
    controller.press(pynput.keyboard.Key.up)
    controller.release(pynput.keyboard.Key.left)
    controller.release(pynput.keyboard.Key.right)
    controller.release(pynput.keyboard.Key.down)
    time.sleep(press_duration)

def left(controller, press_duration = 0.006):
    controller.press(pynput.keyboard.Key.left)
    controller.release(pynput.keyboard.Key.right)
    controller.release(pynput.keyboard.Key.up)
    controller.release(pynput.keyboard.Key.down)
    time.sleep(press_duration)

def right(controller, press_duration = 0.006):
    controller.press(pynput.keyboard.Key.right)
    controller.release(pynput.keyboard.Key.left)
    controller.release(pynput.keyboard.Key.up)
    controller.release(pynput.keyboard.Key.down)
    time.sleep(press_duration)

def reverse(controller, press_duration = 0.006):
    controller.press(pynput.keyboard.Key.down)
    controller.release(pynput.keyboard.Key.up)
    controller.release(pynput.keyboard.Key.right)
    controller.release(pynput.keyboard.Key.left)
    time.sleep(press_duration)

def forward_left(controller, press_duration = 0.006):
    controller.press(pynput.keyboard.Key.up)
    controller.press(pynput.keyboard.Key.left)
    controller.release(pynput.keyboard.Key.right)
    controller.release(pynput.keyboard.Key.down)
    time.sleep(press_duration)
    controller.release(pynput.keyboard.Key.left)

def forward_right(controller, press_duration = 0.006):
    controller.press(pynput.keyboard.Key.up)
    controller.press(pynput.keyboard.Key.right)
    controller.release(pynput.keyboard.Key.down)
    controller.release(pynput.keyboard.Key.left)
    time.sleep(press_duration)
    controller.release(pynput.keyboard.Key.right)

def reverse_left(controller, press_duration = 0.006):
    controller.press(pynput.keyboard.Key.down)
    controller.press(pynput.keyboard.Key.left)
    controller.release(pynput.keyboard.Key.up)
    controller.release(pynput.keyboard.Key.right)
    time.sleep(press_duration)
    controller.release(pynput.keyboard.Key.left)

def reverse_right(controller, press_duration = 0.006):
    controller.press(pynput.keyboard.Key.down)
    controller.press(pynput.keyboard.Key.right)
    controller.release(pynput.keyboard.Key.left)
    controller.release(pynput.keyboard.Key.up)
    time.sleep(press_duration)
    controller.release(pynput.keyboard.Key.right)