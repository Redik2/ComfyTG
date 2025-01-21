import api
import telebot
import prompt_handler
from random import randint
from json import load
import time
import os

token = load(open("config.json", "r"))["token"]

bot = telebot.TeleBot(token)

WATCH_FOLDER = load(open("config.json", "r"))["output_folder"]

@bot.message_handler(commands=['txt2img'])
def txt2img(message: telebot.telebot.types.Message):
    content = message.text

    prompt = prompt_handler.txt2prompt(content)
    prompt["parameters"]["chat_id"] = message.chat.id

    api.send_prompt(model_name=prompt["model"], values=prompt["parameters"])


def send_file_to_chat(file_name, file_path):
    try:
        chat_id = file_name.split('_')[0]
        if not chat_id.isdigit():
            return f"Некорректное имя файла: {file_name}"
        chat_id = int(chat_id)
        with open(file_path, 'rb') as img:
            bot.send_photo(chat_id, img)
        return f"Файл {file_name} отправлен пользователю {chat_id}."
    except Exception as e:
        return f"Ошибка отправки файла {file_name}: {e}"

def check_new_files():
    files = os.listdir(WATCH_FOLDER)
    for file_name in files:
        # Проверяем, является ли файл изображением
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            file_path = os.path.join(WATCH_FOLDER, file_name)
            # Отправляем файл пользователю
            print(send_file_to_chat(file_name, file_path))
            os.rename(WATCH_FOLDER + "\\" + file_name, "sent\\" + str(randint(0, 10 ** 16)) + file_name)
            

def monitor_folder():
    while True:
        check_new_files()
        time.sleep(1)