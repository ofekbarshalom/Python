import time
import keyboard
import pyautogui
import win32api
import win32con

time.sleep(1)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def collect_item(image, color):
    try:
        item_location = pyautogui.locateOnScreen(image, grayscale=color, confidence=0.8)
        if item_location is not None:
            print(f"{image} found")
            # Get the center of the located image
            item_x, item_y = pyautogui.center(item_location)
            click(item_x, item_y)
            return True
    except pyautogui.ImageNotFoundException:
        print(f"{image} not found")


def builderAvailable():
    try:
        if (pyautogui.locateOnScreen('builder1.png', grayscale=True, confidence=0.8) is not None or
                pyautogui.locateOnScreen('builder2.png', grayscale=True, confidence=0.8) is not None):
            print("builder found")
            return True
    except pyautogui.ImageNotFoundException:
        print("builder not found")
        return False


def remove():
    collect_item('remove.png', True)
    time.sleep(0.5)
    collect_item('youNeedMore.png', True)


def removeObject(image, color):
    if collect_item(image, color) and builderAvailable():
        time.sleep(0.5)
        remove()


def removeDecorations():
    removeObject('tree.png', True)
    removeObject('trunk.png', True)
    removeObject('bigTree.png', False)
    removeObject('mushroom.png', True)
    removeObject('greenTree.png', True)


def army():
    pyautogui.keyDown('5')
    time.sleep(0.1)
    pyautogui.keyUp('5')
    time.sleep(0.5)
    collect_item('TrainTroops.png', True)
    for i in range(8):
        collect_item('barbaric.png', True)
    pyautogui.keyDown('5')
    time.sleep(0.1)
    pyautogui.keyUp('5')
    time.sleep(100)


def dropArmy():
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
    collect_item('FindMatch.png', True)
    time.sleep(2)
    dropArmy()
    while not collect_item('ReturnHome.png', True):
        time.sleep(1)
    time.sleep(2)


while not keyboard.is_pressed('q'):
    collect_item('coin.png', True)
    collect_item('elixir.png', True)
    removeDecorations()
    #war()
