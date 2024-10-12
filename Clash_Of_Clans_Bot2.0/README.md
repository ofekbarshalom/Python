# Clash of Clans Bot

This project is a bot for automating gameplay in **Clash of Clans** using **Python**. The bot can collect resources, build structures, manage troops, and perform various in-game actions based on the game state.

## Key Features

- **Image Recognition:** Uses image recognition to locate resources, troops, and in-game prompts on the screen.
  
- **Automated Actions:** Automates actions such as collecting coins and elixir, removing decorations, and managing troops.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/clash-of-clans-bot.git
    ```

2. Install the required dependencies:

    ```bash
    pip install pyautogui keyboard pillow pytesseract
    ```

3. Ensure that you have the necessary image files in the project directory:
    - `builder.png`: Image to detect the builder.
    - `New.png`: Image for new upgrades.
    - `arrow.png`: Image for the arrow prompt.
    - `V.png`: Image for the "V" prompt.
    - `X.png`: Image for the "X" prompt.
    - `remove.png`: Image for the remove button.
    - `youNeedMore.png`: Image for the insufficient resources message.
    - `fullArmy.png`: Image indicating the army is full.
    - `TrainTroops.png`: Image for training troops.
    - `noArmy.png`: Image indicating no army is available.
    - `FindMatch.png`: Image for finding a match.
    - `ReturnHome.png`: Image for returning home.
    - `achievement.png`: Image for achievements.
    - `claimReward.png`: Image for claiming rewards.
    - `season.png`: Image for season rewards.
    - `rewards.png`: Image for rewards in the season.
    - `claim.png`: Image for claiming items.
    - `email.png`: Image for email notifications.
    - `lootCart.png`: Image for loot carts.
    - `collectLootCart.png`: Image for collecting loot carts.
    - `coin.png`: Image for coins.
    - `elixir.png`: Image for elixirs.
    - `grave.png`: Image for graves.

4. Run the project:

    ```bash
    python main.py
    ```

## How It Works

- **Resource Collection:** The bot continuously collects resources such as coins and elixir while scanning the screen for various game elements.

- **Building Structures:** The bot identifies new upgrades and builds structures as needed.

- **Army Management:** The bot trains troops and deploys them during battles, ensuring that actions are performed efficiently.

- **Decorations Removal:** The bot can remove unnecessary decorations to optimize the gameplay area.

- **Loop Until Exit:** The bot continues running until the user presses the 'q' key to stop it.

## Usage

- Start the game and position the game window as required.
- Execute the bot script. The bot will begin detecting game elements and performing actions based on the game state.
- Press 'q' at any time to stop the bot.

## Credits

This bot was developed by Ofek. Feel free to modify and adapt it for your own use!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
