
# Piano Tails Bot

This bot is designed to automate clicks on specific areas of the screen based on pixel color detection. It is intended for use with games or applications where certain conditions (like a specific pixel color) trigger automated actions.

## Features
- **Automated Clicking**: The bot clicks on predefined screen coordinates when it detects a specific pixel color (in this case, black RGB: `(0, 0, 0)`).
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
