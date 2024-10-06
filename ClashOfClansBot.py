import time
import keyboard
import pyautogui
import pytesseract
import win32api
import win32con
from PIL import Image

time.sleep(1)


# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#
#
# def search_word(imagePath, word):
#     try:
#         img = Image.open(imagePath)
#         data = pytesseract.image_to_string(img)
#         for i in range(len(data['text'])):
#             if word.lower() in data['text'][i].lower():
#                 print(f"'{word}' found at ({data['left'][i]}, {data['top'][i]})")
#
#                 # Get the position and dimensions of the word
#                 x = data['left'][i]
#                 y = data['top'][i]
#                 w = data['width'][i]
#                 h = data['height'][i]
#
#                 # Simulate a click at the center of the word
#                 click(x + w // 2, y + h // 2)
#
#                 return True
#
#     except Exception:
#         print("word not found")
#         return False
#
# def screenshot():
#     screenshots = pyautogui.screenshot()
#     screenshots.save(r'C:\Users\ofekb\PycharmProjects\coc_bot\screenshots.png')
#     print("screenshot saved")

#search_word(r'C:\Users\ofekb\PycharmProjects\coc_bot\screenshots.png', 'New')

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def drag_mouse(start_x, start_y, end_x, end_y, duration=1):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=duration)
    pyautogui.mouseUp()


def collect_item(image):
    color = not ((image == 'bigTree.png') or (image == 'achievement.png') or (image == 'New.png')
                 or (image == 'biggerTree.png') or (image == 'sqrStone.png') or (image == 'season.png')
                 or (image == 'email.png') or (image == 'claim.png'))
    confidence = 0.8
    if (image == 'season.png') or (image == 'email.png'):
        confidence = 0.99
    try:
        item_location = pyautogui.locateOnScreen(image, grayscale=color, confidence=confidence)
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


def scan():
    try:
        item_location = pyautogui.locateOnScreen('builder.png', grayscale=True, confidence=0.8)
        if item_location is not None:
            print("scaning")
            item_x, item_y = pyautogui.center(item_location)
            item_y += 230
            #removeDecorations()
            drag_mouse(item_x, item_y, item_x, item_y + 330, 0.5)
            time.sleep(0.4)
            #removeDecorations()
            drag_mouse(item_x, item_y + 300, item_x + 460, item_y, 0.5)
            time.sleep(0.4)
            #removeDecorations()
            drag_mouse(item_x + 60, item_y + 300, item_x - 300, item_y - 300, 0.5)
            time.sleep(0.4)
            #removeDecorations()
            drag_mouse(item_x + 250, item_y - 180, item_x - 250, item_y + 160, 0.5)
            time.sleep(0.4)
            #removeDecorations()
            drag_mouse(item_x + 250, item_y - 180, item_x - 150, item_y + 80, 0.5)
            time.sleep(0.4)
            #removeDecorations()
            drag_mouse(item_x - 350, item_y - 100, item_x + 200, item_y + 450, 0.5)
            time.sleep(0.4)
            #removeDecorations()
            drag_mouse(item_x - 50, item_y + 200, item_x + 200, item_y - 350, 0.5)
            time.sleep(0.4)
            #removeDecorations()

    except pyautogui.ImageNotFoundException:
        print("scaning failed")


def build():
    # search in suggested upgrades New items
    collect_item('builder.png')
    time.sleep(0.2)
    collect_item('New.png')
    time.sleep(2)
    for i in range(15):
        time.sleep(0.05)
        collect_item('arrow.png')
    collect_item('V.png')
    collect_item('X.png')
    # search in shop for New items
    pyautogui.keyDown('1')
    time.sleep(0.1)
    pyautogui.keyUp('1')


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


def make_army():
    pyautogui.keyDown('5')
    time.sleep(0.1)
    pyautogui.keyUp('5')
    time.sleep(0.3)
    if not collect_item('fullArmy.png'):
        collect_item('TrainTroops.png')
        for i in range(20):
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
    while not collect_item('noArmy.png'):
        pyautogui.keyDown('4')
        time.sleep(0.05)
        pyautogui.keyUp('4')


def war():
    make_army()
    pyautogui.keyDown('6')
    time.sleep(0.1)
    pyautogui.keyUp('6')
    time.sleep(0.5)
    collect_item('FindMatch.png')
    time.sleep(2)
    drop_army()
    while not collect_item('ReturnHome.png'):
        time.sleep(1)
    time.sleep(5)


def achievement():
    if collect_item('achievement.png'):
        time.sleep(1)
        collect_item('claimReward.png')
        time.sleep(0.2)
        pyautogui.keyDown('4')
        time.sleep(0.1)
        pyautogui.keyUp('4')


def season():
    if collect_item('season.png'):
        time.sleep(0.5)
        collect_item('rewards.png')
        time.sleep(0.5)
        collect_item('claim.png')
        print("press 4")
        pyautogui.keyDown('4')
        time.sleep(0.1)
        pyautogui.keyUp('4')


def email():
    if collect_item('email.png'):
        time.sleep(0.3)
        pyautogui.keyDown('4')
        time.sleep(0.1)
        pyautogui.keyUp('4')


def loot_cart():
    collect_item('lootCart.png')
    time.sleep(0.2)
    collect_item('collectLootCart.png')


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
    scan()
    time.sleep(0.1)
    season()
    time.sleep(0.2)
    email()
    time.sleep(0.1)
    loot_cart()
    time.sleep(0.1)
    build()
    time.sleep(0.1)
    war()
