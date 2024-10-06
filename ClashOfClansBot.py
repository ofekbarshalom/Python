import time
import keyboard
import pyautogui
import pytesseract
import win32api
import win32con
from PIL import Image

time.sleep(1)

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def collect_item(image):
    color = not ((image == 'bigTree.png') or (image == 'achievement.png') or (image == 'New.png') or (image == 'biggerTree.png') or (image == 'sqrStone.png'))
    try:
        item_location = pyautogui.locateOnScreen(image, grayscale=color, confidence=0.8)
        if item_location is not None:
            print(f"{image} found")
            # Get the center of the located image
            item_x, item_y = pyautogui.center(item_location)
            if image == 'arrow.png':
                item_x -= 100
                item_y += 50
            click(item_x, item_y)
            return True

    except pyautogui.ImageNotFoundException:
        print(f"{image} not found")

def build():
    collect_item('builder.png')
    time.sleep(0.2)
    collect_item('New.png')
    time.sleep(2)
    for i in range(20):
        time.sleep(0.05)
        collect_item('arrow.png')
    collect_item('V.png')
    collect_item('X.png')

def remove():
    collect_item('remove.png')
    time.sleep(0.5)
    collect_item('youNeedMore.png')


def remove_object(image):
    if collect_item(image):
        time.sleep(0.5)
        remove()


def removeDecorations():
    remove_object('tree.png')
    remove_object('trunk.png')
    remove_object('bigTree.png')
    remove_object('mushroom.png')
    remove_object('greenTree.png')
    remove_object('biggerTree.png')
    remove_object('bigStone.png')
    remove_object('longStone.png')
    remove_object('sqrStone.png')
    remove_object('smallStone.png')
    remove_object('roundStone.png')


def army():
    pyautogui.keyDown('5')
    time.sleep(0.1)
    pyautogui.keyUp('5')
    time.sleep(0.5)
    collect_item('TrainTroops.png')
    for i in range(8):
        collect_item('barbaric.png')
    pyautogui.keyDown('5')
    time.sleep(0.1)
    pyautogui.keyUp('5')
    time.sleep(4)


def drop_army():
    time.sleep(1)
    pyautogui.keyDown('6')
    time.sleep(0.1)
    pyautogui.keyUp('6')
    for i in range(21):
        pyautogui.keyDown('4')
        time.sleep(0.1)
        pyautogui.keyUp('4')


def war():
    army()
    pyautogui.keyDown('6')
    time.sleep(0.1)
    pyautogui.keyUp('6')
    time.sleep(0.5)
    collect_item('FindMatch.png')
    time.sleep(2)
    drop_army()
    while not collect_item('ReturnHome.png'):
        time.sleep(1)
    time.sleep(100)


def achievement():
    if collect_item('achievement.png'):
        time.sleep(1)
        collect_item('claimReward.png')
        time.sleep(0.2)
        pyautogui.keyDown('4')
        time.sleep(0.1)
        pyautogui.keyUp('4')


while not keyboard.is_pressed('q'):
    collect_item('coin.png')
    time.sleep(0.1)
    collect_item('elixir.png')
    time.sleep(0.1)
    collect_item('grave.png')
    time.sleep(0.1)
    achievement()
    removeDecorations()
    time.sleep(0.1)
    build()
    time.sleep(0.1)
    war()
