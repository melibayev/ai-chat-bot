# Telegram AI Chatbot 🤖

Welcome to the **Telegram AI Chatbot** project! This bot uses **Gemini AI** to interact with users and provide intelligent responses to their queries. It's designed to help users with various tasks while also logging activity for admin monitoring.

You can try out the bot here: [@chat_ai_talk_bot](https://t.me/chat_ai_talk_bot)

## Features 🚀

- **AI-Powered Conversations**: The bot uses **Gemini AI** to generate human-like responses based on user input.
- **Admin Dashboard**: Admin can view user statistics, including total users, active users for the day, and details such as usernames, first names, and last activity.
- **User Logging**: Logs user activity including username, first name, and the last time they interacted with the bot.
- **Command Support**:
  - `/start`: Welcomes new users and logs them.
  - `/stats`: Displays the total number of users and users who interacted today (admin only).
  - `/list_users`: Displays a list of all users with their details (admin only).

## Technologies 💻

- **Python**: The bot is written in Python, leveraging the `python-telegram-bot` library for Telegram integration.
- **Gemini AI**: The bot uses **Gemini AI** (from Google) to generate responses.
- **Telegram Bot API**: For creating and managing Telegram bots.

## Requirements 📦

Ensure you have the following installed:

- Python 3.7+
- `pip` (Python package manager)

### Required Libraries

The following dependencies are required to run this bot:

- `python-telegram-bot`
- `google-generativeai`
- `python-dotenv`
- `pytz`

## Installation 🛠

1. Clone the repository:

```bash
git clone hhttps://github.com/melibayev/ai-chat-bot.git
```
2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```
3. Install the dependencies:
```bash
pip install -r requirements.txt
```
4. Create a .env file and add your Telegram Bot Token and Gemini AI API key:
```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_ai_api_key
```
## Usage 🚀
1. Run the bot
```bash
python main.py
```
2.Your bot will start and be ready to respond to user queries. Admin commands will be available as well for managing user data and viewing stats.
## Contributing 🤝
Contributions are welcome! Feel free to fork the repository, create a branch, and submit a pull request. Here are some ways you can contribute:
- Add new features or enhance existing ones.
- Fix bugs or improve performance.
- Update documentation.
## License 📜  
This project is licensed under the MIT License - see the [LICENSE](https://github.com/melibayev/ai-chat-bot/blob/main/LICENSE) file for details.