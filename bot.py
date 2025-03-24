import logging
import os
import tempfile
from aiogram import Bot, Dispatcher, executor, types
import yt_dlp

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

SUPPORTED_DOMAINS = ["instagram.com", "tiktok.com", "www.instagram.com", "www.tiktok.com"]

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("📥 أرسل رابط Instagram أو TikTok وسأقوم بتحميل الفيديو لك!")

@dp.message_handler(lambda msg: any(domain in msg.text.lower() for domain in SUPPORTED_DOMAINS))
async def handle_download(message: types.Message):
    url = message.text.strip()
    await message.reply("⏳ جاري تحميل الفيديو، يرجى الانتظار...")

    try:
        temp_dir = tempfile.gettempdir()
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'noplaylist': True,
            'retries': 5,
            'geo_bypass': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            await message.reply_video(
                types.InputFile(filename),
                caption="✅ تم التحميل بنجاح!",
                supports_streaming=True
            )
            os.remove(filename)

    except Exception as e:
        await message.reply(f"❌ تعذر التحميل:\n{str(e)[:400]}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
