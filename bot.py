import telebot
from telebot import types

# === Sizning ma'lumotlaringiz ===
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@kinolarxazinasi"
# ================================

bot = telebot.TeleBot(TOKEN)

# Kino bazasi (kod → kino ro‘yxati)
films = {
    "385": [("Oq Ilon 1 (2019)", "BAACAgIAAyEFAAS0vosPAAMGaLzFCL_DDGrPj_B2_jVkz2gnsBsAAo-LAAImA-FJk1pIJvct9Rk2BA")],
    "777": [("Titanik (1997)", "BAACAgIAAxkBAAIuQ2sQJfRHGz9kTnWvQk9P2sQ0...")]  # misol uchun
}

# Obunani tekshirish funksiyasi
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# Start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        btn2 = types.InlineKeyboardButton("✅ Obuna bo‘ldim", callback_data="check_sub")
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(
            message.chat.id,
            "👋 Assalomu alaykum!\n\n"
            "📽 Kino olish uchun kanalimizga obuna bo‘ling 👇",
            reply_markup=markup
        )
    else:
        bot.send_message(message.chat.id, "✅ Obuna tasdiqlandi! Endi kino kodini yuboring 🎬")

# Callback tugmalarni ishlovchi funksiya
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "check_sub":
        if is_subscribed(call.from_user.id):
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="✅ Rahmat! Siz kanalga obuna bo‘ldingiz.\n\nEndi kino kodini yuboring 🎬"
            )
        else:
            bot.answer_callback_query(call.id, "❌ Hali obuna bo‘lmadingiz!")
    else:
        try:
            # callback_data = "kod_index"
            code, index = call.data.split("_")
            index = int(index) - 1
            title, file_id = films[code][index]

            bot.send_video(call.message.chat.id, file_id, caption=f"🎬 Kino: {title}")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Xatolik: {e}")

# Kod yozilganda film qidirish
@bot.message_handler(func=lambda m: m.text.isdigit())
def search_film(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Botdan foydalanish uchun avval kanalga obuna bo‘ling!")
        return
    
    code = message.text.strip()
    if code in films:
        keyboard = types.InlineKeyboardMarkup()
        for i, (title, file_id) in enumerate(films[code], start=1):
            callback_data = f"{code}_{i}"  # faqat qisqa data
            keyboard.add(types.InlineKeyboardButton(text=f"{i}. {title}", callback_data=callback_data))
        bot.send_message(message.chat.id, f"🔎 Natijalar - {len(films[code])} ta", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "❌ Bunday kod topilmadi.")

# File ID olish (sinov uchun)
@bot.message_handler(content_types=['video'])
def get_file_id(message):
    bot.reply_to(message, f"📂 file_id: {message.video.file_id}")
    print("VIDEO FILE_ID:", message.video.file_id)

# Kanalga tashlangan video uchun file_id olish
@bot.channel_post_handler(content_types=['video'])
def get_channel_file_id(message):
    bot.send_message(message.chat.id, f"📂 file_id (kanal): {message.video.file_id}")
    print("VIDEO FILE_ID (kanal):", message.video.file_id)

print("✅ Bot ishga tushdi...")
bot.polling()
