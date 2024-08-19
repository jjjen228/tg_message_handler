from telethon import TelegramClient
import os
from dotenv import load_dotenv
load_dotenv()

api_id = str(os.getenv('TELEGRAM_API_ID'))
api_hash = str(os.getenv('TELEGRAM_API_HASH'))
phone = str(os.getenv('TELEGRAM_PHONE'))

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=phone)
    print("Successfully logged in!")

client.loop.run_until_complete(main())
