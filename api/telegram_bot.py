import os
import django
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from api.models import TelegramUser
from asgiref.sync import sync_to_async

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_internship.settings')
django.setup()

# --- Helper Functions ---

async def get_or_create_user(username):
    if username is None:
        return None
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(username=username)
    return user

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username
    if username is None:
        await update.message.reply_text('Please set a username in Telegram and try again!')
        return
    await get_or_create_user(username)
    await update.message.reply_text('Welcome! Your username has been saved.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Available commands:\n/start - Start the bot\n/help - Show this help\n/button - Show a custom keyboard')

async def button_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Option 1"), KeyboardButton("Option 2")],
        [KeyboardButton("Option 3")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Choose an option:', reply_markup=reply_markup)
# --- Message Handlers ---

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'You said: {update.message.text}')

async def handle_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    option = update.message.text
    if option in ["Option 1", "Option 2", "Option 3"]:
        await update.message.reply_text(f'You selected: {option}!')
    else:
        await update.message.reply_text('Please use the buttons or commands.')

# --- Main Bot Setup ---

def run(*args, **kwargs):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("button", button_command))

    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_option))
    # Optional: Add a fallback echo handler for debugging
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()
