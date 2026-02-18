import logging
import requests
import io
import random
from aiogram import Bot, Dispatcher, executor, types

# --- AYARLAR ---
API_TOKEN = '8499613617:AAG4wpoQPWr05VevzQNYae6zXj1OLPh5Atk'
QUOTLY_API = "https://bot.lyo.su/quote/generate"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Geniş rəng siyahısı
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

    args = message.get_args().lower().split()
    include_reply = "r" in args
    
    # Rəng təyini (HEX kodları çıxarıldı, ancaq sözlər və qarışıq qaldı)
    bg_color = "#1b1429" 
    if "qarışıq" in args:
        bg_color = "#%06x" % random.randint(0, 0xFFFFFF)
    else:
        for word in args:
            if word in COLORS:
                bg_color = COLORS[word]

    reply_msg = message.reply_to_message
    
    # Profil şəkli götürmə
    avatar_url = ""
    try:
        photos = await bot.get_user_profile_photos(reply_msg.from_user.id, limit=1)
        if photos.total_count > 0:
            file = await bot.get_file(photos.photos[0][0].file_id)
            avatar_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file.file_path}"
    except Exception:
        avatar_url = ""

    # Mesaj strukturu
    msg_obj = {
        "entities": [],
        "avatar": True,
        "from": {
            "id": reply_msg.from_user.id,
            "first_name": reply_msg.from_user.first_name,
            "last_name": reply_msg.from_user.last_name or "",
            "username": reply_msg.from_user.username or "",
            "photo": {"url": avatar_url}
        },
        "text": reply_msg.text or "ᴍᴇᴅɪᴀ",
        "replyMessage": {}
    }

    # Əgər reply ilə bir yerdədirsə (üst-üstə)
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

    try:
        response = requests.post(QUOTLY_API, json=payload, timeout=10)
        if response.status_code == 200:
            sticker = io.BytesIO(response.content)
            sticker.name = "quote.webp"
            await message.answer_sticker(sticker)
        else:
            await message.reply("❌ ᴀᴘɪ xəᴛᴀsı. ʙɪʀ ᴀᴢ sᴏɴʀᴀ ʏᴏxʟᴀʏıɴ.")
    except Exception as e:
        logging.error(f"Xəta: {e}")
        await message.reply("❌ sɪsᴛᴇᴍ xəᴛᴀsı.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
