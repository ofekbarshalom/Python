import time
import cv2
import keyboard
import numpy as np
import pyautogui
import win32api
import win32con
import random

time.sleep(3)

def drag_mouse(start_x, start_y, end_x, end_y, duration=1):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=duration)
    pyautogui.mouseUp()

def find_elixir():
    item_location = pyautogui.locateOnScreen('target.png', grayscale=True, confidence=0.8)
    if item_location is not None:
        print("scaning")
        item_x, item_y = pyautogui.center(item_location)
        drag_mouse(item_x, item_y, item_x, item_y + 200)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def check_size(image):
    try:
        # Capture a screenshot of the screen
        screenshot = pyautogui.screenshot()
        screen_np = np.array(screenshot)  # Convert the screenshot to a NumPy array

        # Convert both the screenshot and the template to grayscale for matching
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)  # Convert screenshot to grayscale

        # Load the template (always in grayscale for template matching)
        template = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

        if template is None:
            print(f"Error: Unable to load image '{image}'. Check the file path and format.")
            return False

        # Try matching the image at different scales (10% to 200%)
        for scale in np.linspace(0.1, 2.0, 40):  # Scale from 10% to 200%
            resized_template = cv2.resize(template, None, fx=scale, fy=scale)
            if resized_template.shape[0] > screen_gray.shape[0] or resized_template.shape[1] > screen_gray.shape[1]:
                continue

            # Match the template with the grayscale screen image
            result = cv2.matchTemplate(screen_gray, resized_template, cv2.TM_CCOEFF_NORMED)

            max_val, max_loc = cv2.minMaxLoc(result)[1:3]  # Get only max_val and max_loc

            if max_val > 0.8:  # Confidence threshold
                print(f"{image} found at scale {scale:.2f}")
                return True

        print(f"{image} not found")
        return False

    except Exception as e:
        print(f"Error: {e}")


def press(image):
    color = not ((image == 'giantGreen.png') or (image == 'bomberGreen.png')
                 or (image == 'witchGreen.png') or (image == 'witch.png'))
    confidence = 0.8
    if ((image == 'giantGreen.png') or (image == 'bomberGreen.png')
             or (image == 'witch.png')):
        confidence = 0.98
    try:
        item_location = pyautogui.locateOnScreen(image, grayscale=color, confidence=confidence)
        if item_location is not None:
            print(f"{image} found")
            # Get the bounding box of the located image
            item_left, item_top, item_width, item_height = item_location
            # Generate random coordinates within the bounding box
            random_x = random.randint(item_left, item_left + item_width - 1)
            random_y = random.randint(item_top, item_top + item_height - 1)
            click(random_x, random_y)
            return True

    except pyautogui.ImageNotFoundException:
        print(f"{image} not found")


def exist(image):
    try:
        item_location = pyautogui.locateOnScreen(image, grayscale=True, confidence=0.8)
        if item_location is not None:
            print(f"{image} found")
            return True

    except pyautogui.ImageNotFoundException:
        print(f"{image} not found")
        return False

def collect_elixir():
    press('elixir.png')
    time.sleep(1)
    if press('collect.png'):
        pyautogui.keyDown('6')
        time.sleep(0.1)
        pyautogui.keyUp('6')


def start_match():
    # Enter match
    pyautogui.keyDown('6')
    time.sleep(0.1)
    pyautogui.keyUp('6')
    time.sleep(1)
    check_size('findNow.png')
    press('findNow.png')
    time.sleep(7)


def drop_army():
    # Drop battle machine
    pyautogui.keyDown('6')
    time.sleep(0.1)
    pyautogui.keyUp('6')
    pyautogui.keyDown('4')
    time.sleep(0.1)
    pyautogui.keyUp('4')

    # Drop giant
    press('giant.png')
    pyautogui.keyDown('4')
    time.sleep(0.1)
    pyautogui.keyUp('4')

    # Drop witches
    press('witch.png')
    for j in range(4):
        pyautogui.keyDown('4')
        time.sleep(0.1)
        pyautogui.keyUp('4')

    # Drop bomber
    press('bomber.png')
    pyautogui.keyDown('4')
    time.sleep(0.1)
    pyautogui.keyUp('4')
    # Activate bomber ability
    press('bomber.png')

    press('giant.png')


while not keyboard.is_pressed('q'):
    find_elixir()
    collect_elixir()
    time.sleep(1)
    start_match()
    drop_army()
    count = 0
    while not exist('returnHome.png'):

        press('bomberGreen.png')

        if not exist('newCard.png'):
            time.sleep(1)

        elif count == 0:
            count = 1
            drop_army()
            press('newCard.png')
            pyautogui.keyDown('4')
            time.sleep(0.1)
            pyautogui.keyUp('4')
            press('newCard.png')

            for i in range(4):
                time.sleep(0.1)
                press('witchGreen.png')

    press('returnHome.png')
    time.sleep(5)
