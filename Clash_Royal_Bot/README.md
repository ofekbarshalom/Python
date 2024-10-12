# Clash Royale Bot

This project is a bot for automating gameplay in **Clash Royale** using **Python**. The bot can identify game elements on the screen and perform actions based on the game state.

## Key Features

- **Image Recognition:** Uses image recognition to locate battle and troop images on the screen.
  
- **Automated Gameplay:** Automates actions such as starting battles and deploying troops based on the current game situation.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/clash-royale-bot.git
    ```

2. Install the required dependencies:

    ```bash
    pip install pyautogui keyboard numpy opencv-python
    ```

3. Ensure that you have the necessary image files in the project directory:
    - `battle.png`: Image to detect the battle screen.
    - `ok.png`: Image to confirm the end of the battle.
    - `LeftBridge.png`: Image for the left bridge.
    - `RightBridge.png`: Image for the right bridge.

4. Run the project:

    ```bash
    python main.py
    ```

## How It Works

- **Image Detection:** The bot uses the `pyautogui` library to capture the screen and look for predefined images to determine the game state.
  
- **Action Execution:** Once the bot identifies the relevant images, it executes mouse clicks and keystrokes to interact with the game, such as starting battles and deploying troops.

- **Loop Until Exit:** The bot continues running until the user presses the 'q' key to stop it.

## Usage

- Start the game and position the game window as required.
- Execute the bot script. The bot will start detecting game elements and performing actions based on the game state.
- Press 'q' at any time to stop the bot.

## Credits

This bot was developed by Ofek. Feel free to modify and adapt it for your own use!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
