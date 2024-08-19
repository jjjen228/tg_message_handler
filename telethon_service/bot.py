from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Message
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
router = Router()
dp = Dispatcher()

dp.include_router(router)

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)

@router.message(Command(commands=['start', 'latest']))
async def send_latest_messages(message: types.Message):
    session = Session()
    messages = session.query(Message).order_by(Message.date.desc()).limit(10).all()
    
    response = ""
    for msg in messages:
        response += (f"{msg.date} - {msg.first_name} {msg.last_name} "
                     f"(@{msg.username}) [ID: {msg.sender_id}]: {msg.text}\n")
    
    await message.answer(response or "No messages found.")

if __name__ == '__main__':
    dp.run_polling(bot)
