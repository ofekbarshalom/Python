# Clash Of Clans Bot

This project is a bot for automating gameplay in **Clash Of Clans** using **Python**. The bot can find and collect elixir, start matches, and deploy troops based on the game state.

## Key Features

- **Image Recognition:** Uses image recognition to locate elixir, troops, and match prompts on the screen.
  
- **Automated Gameplay:** Automates actions such as collecting elixir, starting matches, and deploying troops efficiently.

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
    - `target.png`: Image to detect elixir.
    - `elixir.png`: Image to collect elixir.
    - `collect.png`: Image to confirm elixir collection.
    - `findNow.png`: Image for starting the match.
    - `giant.png`: Image for the Giant troop.
    - `witch.png`: Image for the Witch troop.
    - `bomber.png`: Image for the Bomber troop.
    - `bomberGreen.png`: Image for the Bomber troop in green state.
    - `giantGreen.png`: Image for the Giant troop in green state.
    - `witchGreen.png`: Image for the Witch troop in green state.
    - `newCard.png`: Image for new card prompts.
    - `returnHome.png`: Image for returning home.

4. Run the project:

    ```bash
    python main.py
    ```

## How It Works

- **Elixir Collection:** The bot scans the screen for elixir and collects it by dragging the mouse downwards.
  
- **Match Entry:** The bot initiates a match by pressing the appropriate key and confirming the match prompt.

- **Troop Deployment:** The bot deploys a variety of troops (Giant, Bomber, Witch) at strategic intervals, and can activate troop abilities when required.

- **Loop Until Exit:** The bot continues running until the user presses the 'q' key to stop it.

## Usage

- Start the game and position the game window as required.
- Execute the bot script. The bot will begin detecting game elements and performing actions based on the game state.
- Press 'q' at any time to stop the bot.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
