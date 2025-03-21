import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings
from llama_index.core.agent import ReActAgent

load_dotenv()

TOKEN=os.getenv("TELEGRAM_BOT")
GEMINI_KEY = os.getenv("GEMINI_KEY")

llm = Gemini(
    model="models/gemini-1.5-flash",
    api_key=GEMINI_KEY
)

Settings.llm = llm

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot. How can I help you today?")

# Define a handler for echoing text messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = llm.complete(update.message.text)
    await update.message.reply_text(response.text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a help message!")

async def signup(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await print("Signup")

# Define an error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler("help",help))

    # Add error handler
    application.add_error_handler(error)

    # Start the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()