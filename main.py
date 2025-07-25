import telebot
from telebot.types import ReplyKeyboardMarkup
import requests as rq
import json
import os

bot = telebot.TeleBot("Token")

text = rq.get('https://www.mp3quran.net/api/v3/reciters')
text = json.loads(text.content)

text = text["reciters"]
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True,is_persistent=True)
    for i in text:
        markup.add(i["name"])
    # send the generated markup
    # display this markup:
    bot.send_message(chat_id, 'Select a reciter', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    for  i in text:
        if message.text == i["name"]:
            moshaf = i["moshaf"][0]
            if moshaf["surah_total"] < 114:
                bot.send_message(chat_id, f"this reciter has only {moshaf['surah_total']} surahs")
            surahs = moshaf["surah_list"].split(",")
            
            for j in surahs:
                mp3 = rq.get(moshaf["server"] + str(j).zfill(3) + ".mp3")

                with open(f"{j}.mp3", "wb") as f:
                    f.write(mp3.content)

                os.system("python3 mp3.py " + f"{j}.mp3")
                bot.send_audio(chat_id, audio=open(f"c_{j}.mp3", "rb"))

                os.remove(f"{j}.mp3")
                os.remove(f"c_{j}.mp3")

bot.polling(none_stop=True)
