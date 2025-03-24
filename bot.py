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
    await message.reply("🎬 أرسل رابط فيديو من YouTube وسأقوم بمحاولة تحميله لك بأفضل الخيارات!")

@dp.message_handler(lambda message: "http" in message.text)
async def handle_link(message: types.Message):
    url = message.text.strip()
    await message.reply("⏳ جاري تحميل الفيديو، يرجى الانتظار...")
    try:
        temp_dir = tempfile.gettempdir()
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',         # دمج أفضل فيديو مع أفضل صوت، أو الخيار الأفضل
            'merge_output_format': 'mp4',                  # دمج الناتج في ملف MP4
            'quiet': True,
            'noplaylist': True,
            'geo_bypass': True,                            # تجاوز القيود الجغرافية
            'retries': 10,                                 # زيادة عدد المحاولات
            'fragment_retries': 10,                        # إعادة محاولة تحميل المقاطع المفقودة
            'socket_timeout': 30,                          # مهلة أطول للتواصل مع الخادم
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/115.0.0.0 Safari/537.36',
            'age_limit': 0,                                # تجاهل قيود العمر
            'force_generic_extractor': True,               # استخدام الاستخراج العام إذا لزم الأمر
            'nocheckcertificate': True,                    # تجاهل فحص الشهادات (للتعامل مع مشاكل SSL)
            'skip_unavailable_fragments': True,            # تخطي المقاطع التي لا يمكن تحميلها
            'extract_flat': False,                         # الحصول على معلومات كاملة وليس سطحية
            'quiet': True,
            'progress_hooks': [lambda d: logging.info(d) if d.get("status")=="finished" else None]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            await message.reply_video(types.InputFile(filename), caption="✅ تم تحميل الفيديو بنجاح!")
    except yt_dlp.utils.DownloadError as e:
        await message.reply("❌ هذا الفيديو غير متاح أو مقيّد ولا يمكن تحميله.\nقد يكون محجوبًا جغرافيًا أو يحتاج تسجيل دخول.")
    except Exception as e:
        await message.reply(f"❌ حدث خطأ غير متوقع:\n{str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
