import logging
import os
import random
import tempfile
from aiogram import Bot, Dispatcher, executor, types
import yt_dlp

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# إعدادات الذكاء الاصطناعي للتحايل على القيود
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36"
]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("🦾 أرسل رابط اليوتيوب وسأحاول اختراق القيود الذكية!")

@dp.message_handler(lambda message: "youtube.com" in message.text.lower() or "youtu.be" in message.text.lower())
async def handle_link(message: types.Message):
    url = message.text.strip()
    await message.reply("⚡ جاري تنشيط بروتوكولات التجاوز...")
    
    try:
        temp_dir = tempfile.gettempdir()
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'ignoreerrors': True,
            'geo_bypass': True,
            'geo_bypass_country': random.choice(['US', 'DE', 'FR', 'JP']),
            'referer': 'https://www.youtube.com/',
            'retries': 15,
            'fragment_retries': 15,
            'socket_timeout': 60,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['hls', 'dash']
                }
            },
            'user_agent': random.choice(USER_AGENTS),
            'nocheckcertificate': True,
            'force_ipv4': True,
            'throttledratelimit': 1000000,
            'http_headers': {
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Mode': 'navigate'
            },
            'overwrites': True,
            'verbose': False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if not info:
                return await message.reply("🔒 الفيديو محمي بنظام حماية متقدم - جرب استخدام رابط مختصر")
                
            filename = ydl.prepare_filename(info)
            
            await message.reply_video(
                types.InputFile(filename),
                caption="✅ تم التحميل بنجاح باستخدام الذكاء البنائي!",
                supports_streaming=True
            )
            
            os.remove(filename)
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e).lower()
        if 'age restricted' in error_msg:
            await message.reply("🔞 لحل قيود العمر:\n1. استخدم الرابط عبر متصفح TOR\n2. أضف '&has_verified=1' لنهاية الرابط")
        elif 'private' in error_msg:
            await message.reply("🔐 للفيديوهات الخاصة:\n1. أضف كلمة السر بعد الرابط\n2. استخدم تقنية الرابط الشبح (مثال: youtu.be/XXXXX)")
        else:
            await message.reply(f"⚠️ خطأ تقني: {str(e)[:150]}")

    except Exception as e:
        await message.reply(f"💥 خطأ غير متوقع: {str(e)[:100]}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
