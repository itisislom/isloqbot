import os
import telebot

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

# Проверка токена
if not TOKEN or ":" not in TOKEN:
    raise ValueError("BOT_TOKEN is missing or invalid. Please set it in Render environment variables.")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    try:
        with open("users.txt", "a+") as f:
            f.seek(0)
            if str(user_id) not in f.read():
                f.write(str(user_id) + "\n")
        bot.send_message(user_id, "Siz yangiliklarga obuna bo'lgansiz!")
    except Exception as e:
        bot.send_message(user_id, "Yangilikga obuna bo'lishda xato!")
        print(f"Hatolik yuz berdi!: {e}")

@bot.message_handler(commands=['send'])
def handle_send(message):
    ADMIN_ID = 8037600402
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "Sizning huquqingiz yo'q!")
        return

    text_to_send = "Bizda Android qurilmalari uchun ilovamiz borligini bilarmidingiz? 👀 Telegram kanalimizga o'tib tekshiring: @isloqapp"
    try:
        with open("users.txt", "r") as f:
            users = f.readlines()
        success = 0
        for user_id in users:
            try:
                bot.send_message(int(user_id.strip()), text_to_send)
                success += 1
            except:
                continue
        bot.send_message(message.chat.id, f"Yangiliklar tugadi, jo'natildi {success} foydalanuvchilarga")
    except Exception as e:
        bot.send_message(message.chat.id, f"Yangilik jo'natishda hatolik yuz berdi. {e}")

print("BOT ISHGA TUSHIRILDI")
bot.polling()
