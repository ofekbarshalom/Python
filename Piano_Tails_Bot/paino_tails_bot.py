import time
import json
from pathlib import Path
import keyboard
import pyautogui
import win32api
import win32con


DEFAULT_CONFIG = {
    "stop_key": "q",
    "target_red_value": 0,
    "click_delay": 0.01,
    "lanes": [
        {"check": [1800, 516], "click": [1800, 530]},
        {"check": [1903, 516], "click": [1903, 530]},
        {"check": [1981, 516], "click": [1981, 530]},
        {"check": [2115, 516], "click": [2115, 530]}
    ]
}


def load_config(config_path):
    if not config_path.exists():
        config_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
        print(f"Config file was created at: {config_path}")
        print("Update lane coordinates in the config and run again for your screen.")

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)

def click(x, y, delay):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(delay)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def main():
    project_dir = Path(__file__).resolve().parent
    config_path = project_dir / "bot_config.json"
    config = load_config(config_path)

    stop_key = config.get("stop_key", "q")
    target_red_value = config.get("target_red_value", 0)
    click_delay = float(config.get("click_delay", 0.01))
    lanes = config.get("lanes", [])

    if not lanes:
        raise ValueError("No lanes found in bot_config.json")

    print(f"Bot started. Press '{stop_key}' to stop.")
    while not keyboard.is_pressed(stop_key):
        for lane in lanes:
            check_x, check_y = lane["check"]
            click_x, click_y = lane["click"]

            if pyautogui.pixel(check_x, check_y)[0] == target_red_value:
                click(click_x, click_y, click_delay)


if __name__ == "__main__":
    main()
