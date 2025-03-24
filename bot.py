import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from pytube import YouTube
import yt_dlp
import tempfile

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("🎬 أرسل رابط YouTube أو TikTok وسأقوم بتحميله لك!")


@dp.message_handler(lambda message: "http" in message.text)
async def handle_link(message: types.Message):
    url = message.text.strip()

    await message.reply("⏳ جاري تحميل الفيديو، يرجى الانتظار...")

    try:
        if "tiktok.com" in url:
            await download_tiktok(message, url)
        elif "youtube.com" in url or "youtu.be" in url:
            await download_youtube(message, url)
        else:
            await message.reply("❌ الرابط غير مدعوم حالياً.")
    except Exception as e:
        await message.reply(f"❌ حدث خطأ أثناء التحميل:\n{str(e)}")


async def download_youtube(message, url):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
        stream.download(filename=tmp_file.name)
        await message.reply_video(types.InputFile(tmp_file.name), caption=f"✅ تم تحميل الفيديو من YouTube")


async def download_tiktok(message, url):
    ydl_opts = {
        'outtmpl': tempfile.gettempdir() + '/%(id)s.%(ext)s',
        'format': 'mp4',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        await message.reply_video(types.InputFile(filename), caption=f"✅ تم تحميل الفيديو من TikTok")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
