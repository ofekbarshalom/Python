# Gaslight GPT

A CLI chatbot that you can gaslight GPT into believing it said things it never did.

## How It Works

1. You chat with GPT-4o in the terminal.
2. Every message (yours and GPT's) is saved to `conversation.csv`.
3. Between messages, you can open the CSV and edit any previous response.
4. GPT reloads the CSV before each reply, so it takes the edited history at face value.

## Setup

1. Install dependencies:
   ```
   pip install openai python-dotenv
   ```

2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-key-here
   ```

3. Run it:
   ```
   python main.py
   ```

## Commands

| Command  | Description              |
|----------|--------------------------|
| `/quit`  | Exit the chat            |
| `/reset` | Clear conversation history |
