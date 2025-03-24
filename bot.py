import logging
import os
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("مرحباً! أرسل لي رابط فيديو من YouTube أو TikTok للتحميل.")

@dp.message_handler(lambda message: "http" in message.text)
async def handle_link(message: types.Message):
    await message.reply("جارٍ المعالجة... (التحميل لم يُفعّل بعد)")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
