#This is a Paino tails bot
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

#X: 1783 Y:  516 RGB: (185, 189, 235)
#X: 1879 Y:  516 RGB: (181, 184, 235)
#X: 2005 Y:  525 RGB: (180, 183, 235)
#X: 2129 Y:  517 RGB: (  0,   0,   0)

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

while keyboard.is_pressed('q') ==   False:

    if pyautogui.pixel(1800, 516)[0] == 0:
        click(1800,530)
    if pyautogui.pixel(1903, 516)[0] == 0:
        click(1903,530)
    if pyautogui.pixel(1981, 516)[0] == 0:
        click(1981,530)
    if pyautogui.pixel(2115, 516)[0] == 0:
        click(2115,530)

