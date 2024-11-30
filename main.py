import logging
import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from datetime import datetime
import pytz
import json

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token and Gemini API key from .env variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configuration Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Path to store user data and admin info
USERS_LOG_FILE = "users.json"
ADMIN_FILE = "admin.json"

# Timezone for Tashkent
TASHKENT_TZ = pytz.timezone("Asia/Tashkent")

# Function to get the admin ID from the file
def get_admin():
    if os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "r") as file:
            return json.load(file).get("admin_id")
    return None

# Function to set the admin ID (only set once)
def set_admin(user_id):
    if not os.path.exists(ADMIN_FILE):  # Set admin only once
        with open(ADMIN_FILE, "w") as file:
            json.dump({"admin_id": user_id}, file)

# User logging function
def log_user_data(user):
    # Get the current time in the server's timezone and convert it to Tashkent(depends on pytz option) time
    server_time = datetime.now()
    tashkent_time = server_time.astimezone(TASHKENT_TZ)

    user_data = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "timestamp": tashkent_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    try:
        # Read existing data
        if os.path.exists(USERS_LOG_FILE):
            with open(USERS_LOG_FILE, "r") as file:
                users = json.load(file)
        else:
            users = []

        # Update the timestamp if the user already exists
        for existing_user in users:
            if existing_user["user_id"] == user_data["user_id"]:
                existing_user["timestamp"] = user_data["timestamp"]
                break
        else:
            # Add new user if not found
            users.append(user_data)

        # Write updated data back to the file
        with open(USERS_LOG_FILE, "w") as file:
            json.dump(users, file, indent=4)

    except Exception as e:
        logger.error(f"Error logging user data: {e}")

# Command to list users and total counts
def list_users(update: Update, context: CallbackContext):
    user = update.effective_user
    admin_id = get_admin()

    if user.id != admin_id:
        update.message.reply_text("❌ You don't have permission to use this command.")
        return

    try:
        if os.path.exists(USERS_LOG_FILE):
            with open(USERS_LOG_FILE, "r") as file:
                users = json.load(file)

            if not users:
                update.message.reply_text("No users have used the bot yet.")
                return

            # Calculate total users and users who used the bot today
            total_users = len(users)
            today_users = sum(
                1 for u in users if
                datetime.strptime(u['timestamp'], "%Y-%m-%d %H:%M:%S").date() == datetime.now(TASHKENT_TZ).date()
            )

            # Preparing the response
            response = f"📊 Total users: {total_users}\n"
            response += f"🌍 Users who used today: {today_users}\n\n"
            response += "📋 List of users who used the bot:\n\n"
            for u in users:
                response += (
                    f"👤 User ID: {u['user_id']}\n"
                    f"   Username: @{u['username'] or 'N/A'}\n"
                    f"   First Name: {u['first_name']}\n"
                    f"   Last Active: {u['timestamp']}\n\n"
                )
            update.message.reply_text(response)
        else:
            update.message.reply_text("No user log file found. No users have used the bot yet.")
    except Exception as e:
        logger.error(f"Error reading user log file: {e}")
        update.message.reply_text("⚠️ An error occurred while retrieving user data.")

# Function to interact with AI
def chat_with_gemini(user_message: str) -> str:
    try:
        # Generate content based on user input
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        logger.error(f"Error with Gemini AI request: {e}")
        return "Sorry, there was an error while processing your request."

# Command to start the bot
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    log_user_data(user)  # Log user data

    # Check if admin is set, if not, set the first user as admin
    if get_admin() is None:
        set_admin(user.id)
        update.message.reply_text("👑 You have been set as the admin!")
    else:
        update.message.reply_text("Hello! Welcome to the AI Chat Bot! 🤖\n\n"
        "I’m here to assist you with any questions💬\n\n"
        "Ready to chat? Let's get started! 😊")

# Command to send statistics to the admin
def stats(update: Update, context: CallbackContext):
    user = update.message.from_user
    admin_id = get_admin()

    if user.id != admin_id:
        update.message.reply_text("❌ You don't have permission to use this command.")
        return

    try:
        if os.path.exists(USERS_LOG_FILE):
            with open(USERS_LOG_FILE, "r") as file:
                users = json.load(file)

            total_users = len(users)
            today_users = sum(
                1 for u in users if
                datetime.strptime(u['timestamp'], "%Y-%m-%d %H:%M:%S").date() == datetime.now(TASHKENT_TZ).date()
            )

            response = f"📊 **User Statistics**\n"
            response += f"Total users: {total_users}\n"
            response += f"Users who interacted today: {today_users}\n\n"
            update.message.reply_text(response)
        else:
            update.message.reply_text("No user log file found. No users have used the bot yet.")
    except Exception as e:
        logger.error(f"Error retrieving stats: {e}")
        update.message.reply_text("⚠️ An error occurred while retrieving user stats.")


# Function to handle user messages
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text  # Get user's message
    logger.info(f"Received message: {user_message}")

    # Get the response from Gemini AI
    ai_response = chat_with_gemini(user_message)

    # Send Gemini AI's response back to the user
    update.message.reply_text(ai_response)

# Main function to run the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stats", stats))  # Admin stats command
    dp.add_handler(CommandHandler("list_users", list_users))  # Admin list users command
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    logger.info("Bot is running...")
    updater.idle()

# Run the bot
if __name__ == "__main__":
    main()
