import logging
import os
import tempfile
from aiogram import Bot, Dispatcher, executor, types
import yt_dlp

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("🎬 أرسل رابط فيديو وسأقوم بتحميله لك باستخدام yt-dlp!")

@dp.message_handler(lambda message: "http" in message.text)
async def handle_link(message: types.Message):
    url = message.text.strip()
    await message.reply("⏳ جاري تحميل الفيديو...")

    try:
        temp_dir = tempfile.gettempdir()
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            await message.reply_video(types.InputFile(filename), caption="✅ تم التحميل بنجاح!")
    except Exception as e:
        await message.reply(f"❌ حدث خطأ أثناء التحميل:\n{str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
