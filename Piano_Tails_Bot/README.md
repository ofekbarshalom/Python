
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

## How It Works

1. **Pixel Detection**: The bot continuously monitors pixel colors at certain coordinates on the screen.
   - The coordinates are hardcoded in the script and correspond to specific points on the screen. If the RGB color of the pixel at these coordinates matches black (`(0, 0, 0)`), the bot triggers a click action at those positions.
2. **Clicking**: The bot moves the cursor to the detected location and simulates a mouse click.

### Screen Coordinates
The following screen coordinates are monitored for pixel color changes:

- **Position 1**: X: 1800, Y: 516
- **Position 2**: X: 1903, Y: 516
- **Position 3**: X: 1981, Y: 516
- **Position 4**: X: 2115, Y: 516
