from pyautogui import *
import pyautogui
import time
import keyboard
import random
import numpy as np
import win32api, win32con

time.sleep(2)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


#dropTroop
def selectTroop():
    random_troop = random.randint(1, 4)
    pyautogui.keyDown(str(random_troop))
    time.sleep(0.1)
    pyautogui.keyUp(str(random_troop))


while not keyboard.is_pressed('q'):
    # Start battle
    try:
        if pyautogui.locateOnScreen('battle.png', grayscale=True, confidence=0.8) is not None:
            print("battle found")
            click(1880, 857)
            time.sleep(3)
    except pyautogui.ImageNotFoundException:
        print("battle not found exception")

    # End battle
    try:
        if pyautogui.locateOnScreen('ok.png', grayscale=True, confidence=0.8) is not None:
            print("ok found")
            click(1875, 1108)
            time.sleep(2)
    except pyautogui.ImageNotFoundException:
        print("ok not found exception")

    # Troops on right bridge
    try:
        if pyautogui.locateOnScreen('LeftBridge.png', grayscale=True, confidence=0.8) is not None:
            print("Left Bridge not found")

    except pyautogui.ImageNotFoundException:
        print("Left Bridge found")
        selectTroop()
        random_x = random.randint(1644, 1783)
        random_y = random.randint(673, 697)
        click(random_x, random_y)
        time.sleep(1)

    # Troops on right bridge
    try:
        if pyautogui.locateOnScreen('RightBridge.png', grayscale=True, confidence=0.8) is not None:
            print("Right Bridge not found")

    except pyautogui.ImageNotFoundException:
        print("Right Bridge found")
        selectTroop()
        random_x = random.randint(1958, 2101)
        random_y = random.randint(673, 697)
        click(random_x, random_y)
        time.sleep(0.5)
