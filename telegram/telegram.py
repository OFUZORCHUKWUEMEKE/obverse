import os
from dotenv import load_dotenv

load_dotenv() 
telegram_bot_token = os.getenv("TELEGRAM_BOT")

print(telegram_bot_token);



