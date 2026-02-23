
# Piano Tails Bot

This bot is designed to automate clicks on specific areas of the screen based on pixel color detection. It is intended for use with games or applications where certain conditions (like a specific pixel color) trigger automated actions.

## Features
- **Config-Based Coordinates**: Lane coordinates are stored in `bot_config.json` so you can adapt the bot to your own screen without editing Python code.
- **Automated Clicking**: The bot clicks on configured screen coordinates when it detects a target pixel color.
- **Real-time Monitoring**: It continuously checks pixel colors in specific locations, clicking on those coordinates if the conditions are met.
- **Keyboard Control**: You can stop the bot by pressing the `q` key.

## Requirements

Ensure you have the following Python packages installed:

- `pyautogui`
- `keyboard`
- `pywin32`

You can install the necessary packages using `pip`:

```bash
pip install pyautogui keyboard pywin32
```

## Configuration

Before running, update `bot_config.json` to match your monitor and game window position.

- `stop_key`: key used to stop the bot.
- `target_red_value`: red-channel value to trigger a click (default `0` for black tiles).
- `click_delay`: delay between mouse down and up.
- `lanes`: each lane has:
	- `check`: pixel coordinates to detect tile color.
	- `click`: coordinates where the bot should click.

## Run

From the `Piano_Tails_Bot` folder:

```bash
python paino_tails_bot.py
```

Press `q` (or your configured `stop_key`) to stop the bot.
