# Ofek's Telegram Bot

This is a Telegram bot built using the `python-telegram-bot` library. The bot can respond to text messages and handle simple commands like `/start`, `/help`, and a custom command.

## Features

- Responds to text messages with simple replies.
- Supports three commands:
  - `/start`: Greets the user.
  - `/help`: Provides a short description of the bot.
  - `/custom`: A custom command that replies with a predefined message.
- Detects whether the bot is mentioned in group chats.
  
## Requirements

- Python 3.10+
- `python-telegram-bot` library

## Installation

1. Clone this repository:
    ```bash
    git clone <repository-url>
    ```
   Replace `<repository-url>` with the actual URL of your GitHub repository.

2. Navigate to the project directory:
    ```bash
    cd <repository-directory>
    ```

3. Install the required dependencies using `pip`:
    ```bash
    pip install python-telegram-bot
    ```

4. Set your bot's token in the code:
   - Replace `'Enter_secret_token_here'` with your actual Telegram bot token in the `TOKEN` variable.

## License

This project is licensed under the MIT License.
