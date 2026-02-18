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

# Hazır rəng adları
COLORS = {
    "mavi": "#0000FF", "qırmızı": "#FF0000", "yaşıl": "#00FF00",
    "sarı": "#FFFF00", "qara": "#000000", "ağ": "#FFFFFF",
    "bənövşəyi": "#8A2BE2", "çəhrayı": "#FF69B4", "narıncı": "#FFA500",
    "boz": "#808080", "qəhvəyi": "#A52A2A", "tünd": "#1b1429"
}

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(
        "👋 **Salam! Mən mesajları stikerə çevirən botam.**\n\n"
        "İstifadə qaydasını öyrənmək üçün /helpq yazın."
    )

@dp.message_handler(commands=['helpq'])
async def help_command(message: types.Message):
    help_text = (
        "📖 **Botdan İstifadə Qaydası:**\n\n"
        "1️⃣ **Sadə stiker:** Bir mesajı reply edib `/q` yazın.\n"
        "2️⃣ **Reply ilə birlikdə:** Mesajı reply edib `/q r` yazın.\n"
        "3️⃣ **Rəngli stiker:** `/q mavi` və ya `/q r qırmızı` yazın.\n"
        "4️⃣ **Xüsusi rəng (HEX):** Məsələn: `/q #4287f5` və ya `/q r #4287f5`\n"
        "5️⃣ **Qarışıq rəng:** `/q qarışıq` yazsanız bot təsadüfi rəng seçəcək.\n\n"
        "🎨 **Mövcud adlar:** mavi, qırmızı, yaşıl, sarı, qara, ağ, bənövşəyi, çəhrayı, narıncı, boz, tünd."
    )
    await message.reply(help_text, parse_mode="Markdown")

@dp.message_handler(commands=['q'])
async def quote_handler(message: types.Message):
    if not message.reply_to_message:
        return await message.reply("⚠️ Zəhmət olmasa bir mesajı reply (cavab) edin!")

    args = message.get_args().lower().split()
    include_reply = "r" in args
    
    # Rəng təyini
    bg_color = "#1b1429" # Standart tünd rəng
    
    if "qarışıq" in args:
        bg_color = "#%06x" % random.randint(0, 0xFFFFFF)
    else:
        for word in args:
            if word in COLORS:
                bg_color = COLORS[word]
            elif word.startswith("#") and len(word) == 7: # HEX kod yoxlaması
                bg_color = word

    reply_msg = message.reply_to_message
    
    # İstifadəçi şəkli
    photos = await bot.get_user_profile_photos(reply_msg.from_user.id, limit=1)
    avatar_url = ""
    if photos.total_count > 0:
        file = await bot.get_file(photos.photos[0][0].file_id)
        avatar_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file.file_path}"

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
        "text": reply_msg.text or "Media",
        "replyMessage": {}
    }

    # Üst mesaj (Reply) əlavə edilməsi
    if include_reply and reply_msg.reply_to_message:
        upper_msg = reply_msg.reply_to_message
        msg_obj["replyMessage"] = {
            "name": upper_msg.from_user.full_name,
            "text": upper_msg.text or "Media content",
            "chatId": upper_msg.from_user.id
        }

    payload = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": bg_color,
        "messages": [msg_obj]
    }

    try:
        response = requests.post(QUOTLY_API, json=payload)
        if response.status_code == 200:
            sticker = io.BytesIO(response.content)
            sticker.name = "quote.webp"
            await message.answer_sticker(sticker)
        else:
            await message.reply("❌ API xətası. Bir az sonra yoxlayın.")
    except Exception as e:
        logging.error(f"Xəta: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
