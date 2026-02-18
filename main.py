import logging
import aiohttp # Asinxron sorğular üçün
import io
import random
from aiogram import Bot, Dispatcher, executor, types

# --- AYARLAR ---
API_TOKEN = '8499613617:AAG4wpoQPWr05VevzQNYae6zXj1OLPh5Atk'
QUOTLY_API = "https://bot.lyo.su/quote/generate" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Bütün rənglər
COLORS = {
    "mavi": "#0000FF", "qırmızı": "#FF0000", "yaşıl": "#00FF00",
    "sarı": "#FFFF00", "qara": "#000000", "ağ": "#FFFFFF",
    "bənövşəyi": "#8A2BE2", "çəhrayı": "#FF69B4", "narıncı": "#FFA500",
    "boz": "#808080", "qəhvəyi": "#A52A2A", "tünd": "#1b1429",
    "turkuaz": "#40E0D0", "qızılı": "#FFD700"
}

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(
        "👋 sᴀʟᴀᴍ! ᴍəɴ ᴍᴇsᴀᴊʟᴀʀı sᴛɪᴋᴇʀə çᴇᴠɪʀəɴ ʙᴏᴛᴀᴍ.\n\n"
        "ɪsᴛɪғᴀᴅə ǫᴀʏᴅᴀsını öʏʀəɴᴍəᴋ üçüɴ /helpq ʏᴀᴢıɴ."
    )

@dp.message_handler(commands=['helpq'])
async def help_command(message: types.Message):
    help_text = (
        "📖 ʙᴏᴛᴅᴀɴ ɪsᴛɪғᴀᴅə ǫᴀʏᴅᴀsı:\n\n"
        "1️⃣ sᴀᴅə sᴛɪᴋᴇʀ: ʙɪʀ ᴍᴇsᴀᴊı ʀᴇᴘʟʏ ᴇᴅɪʙ /q ʏᴀᴢıɴ.\n"
        "2️⃣ ʀᴇᴘʟʏ ɪʟə ʙɪʀʟɪᴋᴅə: ᴍᴇsᴀᴊı ʀᴇᴘʟʏ ᴇᴅɪʙ /q r ʏᴀᴢıɴ.\n"
        "3️⃣ ʀəɴɢʟɪ sᴛɪᴋᴇʀ: /q ᴍᴀᴠɪ ᴠə ʏᴀ /q r ǫıʀᴍıᴢı ʏᴀᴢıɴ.\n"
        "4️⃣ ǫᴀʀışıǫ ʀəɴɢ: /q ǫᴀʀışıǫ ʏᴀᴢsᴀɴız ʙᴏᴛ ᴛəsᴀᴅüғɪ ʀəɴɢ sᴇçəᴄəᴋ.\n\n"
        "🎨 ᴍöᴠᴄᴜᴅ ᴀᴅʟᴀʀ: ᴍᴀᴠɪ, ǫıʀᴍıᴢı, ʏᴀşıʟ, sᴀʀı, ǫᴀʀᴀ, ᴀğ, ʙəɴöᴠşəʏɪ, çəʜʀᴀʏı, ɴᴀʀıɴᴄı, ʙᴏᴢ, ᴛüɴᴅ, ᴛᴜʀᴋᴜᴀᴢ, ǫıᴢıʟı."
    )
    await message.reply(help_text)

@dp.message_handler(commands=['q'])
async def quote_handler(message: types.Message):
    if not message.reply_to_message:
        return await message.reply("⚠️ ᴢəʜᴍəᴛ ᴏʟᴍᴀsᴀ ʙɪʀ ᴍᴇsᴀᴊı ʀᴇᴘʟʏ ᴇᴅɪɴ!")

    await bot.send_chat_action(message.chat.id, types.ChatActions.CHOOSE_STICKER)

    args = message.get_args().lower().split()
    include_reply = "r" in args
    bg_color = "#1b1429" 
    
    if "qarışıq" in args:
        bg_color = "#%06x" % random.randint(0, 0xFFFFFF)
    else:
        for word in args:
            if word in COLORS:
                bg_color = COLORS[word]

    reply_msg = message.reply_to_message
    
    msg_obj = {
        "entities": [],
        "avatar": True,
        "from": {
            "id": reply_msg.from_user.id,
            "first_name": reply_msg.from_user.first_name,
            "last_name": reply_msg.from_user.last_name or "",
            "username": reply_msg.from_user.username or "",
            "photo": {} 
        },
        "text": reply_msg.text or "ᴍᴇᴅɪᴀ",
        "replyMessage": {}
    }

    if include_reply and reply_msg.reply_to_message:
        upper_msg = reply_msg.reply_to_message
        msg_obj["replyMessage"] = {
            "name": upper_msg.from_user.full_name,
            "text": upper_msg.text or "ᴍᴇᴅɪᴀ ᴄᴏɴᴛᴇɴᴛ",
            "chatId": upper_msg.from_user.id
        }

    payload = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": bg_color,
        "messages": [msg_obj]
    }

    # API-ni aldatmaq üçün başlıqlar (Headers)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    }

    # Asinxron aiohttp istifadəsi
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(QUOTLY_API, json=payload, timeout=25) as response:
                if response.status == 200:
                    content = await response.read()
                    if content:
                        sticker = io.BytesIO(content)
                        sticker.seek(0)
                        sticker.name = "quote.webp"
                        await message.answer_sticker(sticker)
                    else:
                        await message.reply("❌ API cavabı boşdur.")
                elif response.status == 403:
                     await message.reply("🚫 API Heroku IP-sini tamamilə bloklayıb. Headers kömək etmədi.")
                else:
                    await message.reply(f"❌ ᴀᴘɪ xəᴛᴀsı: {response.status}")
    except Exception as e:
        logging.error(f"Xəta: {e}")
        await message.reply("❌ sɪsᴛᴇᴍ xəᴛᴀsı. ʙᴀğʟᴀɴᴛı ᴋəsɪʟᴅɪ.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
