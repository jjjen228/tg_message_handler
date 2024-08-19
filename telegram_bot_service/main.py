from telethon import TelegramClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Message
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()

api_id = str(os.getenv('TELEGRAM_API_ID'))
api_hash = str(os.getenv('TELEGRAM_API_HASH'))
phone = str(os.getenv('TELEGRAM_PHONE'))
db_url = str(os.getenv('DATABASE_URL'))

client = TelegramClient('session_name', api_id, api_hash)

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
async def main():
    await client.start(phone=phone)
    
    session = Session()
    async for dialog in client.iter_dialogs():
        if dialog.is_user:
            async for message in client.iter_messages(dialog.id):
                if message.date > utc_now - timedelta(minutes=5):
                    msg = Message(
                        message_id=message.id,
                        text=message.text,
                        sender_id=message.sender_id,
                        first_name=message.sender.first_name,
                        last_name=message.sender.last_name,
                        username=message.sender.username,
                        phone_number=message.sender.phone,
                        date=message.date
                    )
                    session.add(msg)
    session.commit()

client.loop.run_until_complete(main())
