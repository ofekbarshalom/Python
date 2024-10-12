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

## Usage

1. Start the bot by running the Python script:
    ```bash
    python <script-name>.py
    ```
   Replace `<script-name>` with the name of your Python script.

2. The bot will be active and respond to the following commands:
   - `/start` - Sends a welcome message.
   - `/help` - Sends a help message.
   - `/custom` - Sends a custom message.

3. Send any other message, and the bot will respond based on the message content.

## Example Responses

- Send "hello" or "hi", and the bot will reply with "Hey there!"
- Ask "How are you?", and the bot will reply with "I am good!"
- If the bot doesn't understand, it will reply with "I do not understand what you wrote."

## License

This project is licensed under the MIT License.
