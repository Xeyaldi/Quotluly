import logging
import io
import random
import textwrap
from aiogram import Bot, Dispatcher, executor, types
from PIL import Image, ImageDraw, ImageFont

# --- AYARLAR ---
API_TOKEN = '8499613617:AAG4wpoQPWr05VevzQNYae6zXj1OLPh5Atk'

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

# Font yolu (repo-da fonts qovluğunda saxlayın)
FONT_PATH = "fonts/Roboto-Regular.ttf"

# 🔹 Lokal stiker generatoru
def make_sticker(text, bg_color):
    img = Image.new("RGBA", (512, 512), bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 40)
    wrapped = textwrap.fill(text, 18)
    draw.text((256, 256), wrapped, font=font, fill="white", anchor="mm")
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    bio.name = "sticker.png"
    return bio

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
    text = reply_msg.text or "ᴍᴇᴅɪᴀ"

    # 🔹 Lokal stiker yaradılır (API çıxarıldı)
    try:
        sticker = make_sticker(text, bg_color)
        await message.answer_sticker(sticker)
    except Exception as e:
        logging.error(f"Xəta: {e}")
        await message.reply("❌ Stiker yaradıla bilmədi. Font mövcuddurmu?")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
