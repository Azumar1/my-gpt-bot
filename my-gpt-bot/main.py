import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.dispatcher.router import Router
from aiogram.client.default import DefaultBotProperties
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка токенов из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка на ошибки
if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ Не найдены токены. Убедитесь, что .env файл заполнен.")

# Инициализация бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# OpenAI клиент
client = OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я GPT-бот. Напиши сообщение — я отвечу.")

# Ответ на любое сообщение
@router.message()
async def handle_message(message: Message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        print("[OpenAI ERROR]", e)
        await message.answer("❌ Ошибка при обращении к OpenAI.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())