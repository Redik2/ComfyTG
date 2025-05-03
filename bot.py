import api
import telebot
import prompt_handler
from random import randint
from json import load
import time
import os

token = load(open("config.json", "r"))["tg_token"]

bot = telebot.TeleBot(token)
system_prompt = open("system.txt", 'r', encoding="utf-8").read()
history = [{"role": "system", "content": system_prompt}]

parameters = {}

WATCH_FOLDER = load(open("config.json", "r"))["output_folder"]

@bot.message_handler()
def on_message(message: telebot.telebot.types.Message):
    global parameters, history
    content = message.text
    print(content)
    if content.startswith('/config'):
        parameters = prompt_handler.txt2parameters(content)
        print(f"new parameters: {parameters}")
        return
    elif content.startswith('/clear'):
        history = [{"role": "system", "content": system_prompt}]
        return
    elif content.startswith('/hide'):
        bot.send_message(message.chat.id, ".\n" * 50)
        return
    elif content.startswith('.'):
        return
    
    prompt = {"parameters": parameters.copy(), "model": parameters['model']}
    prompt["parameters"]["chat_id"] = message.chat.id
    prompt['parameters'].pop('model')

    msg = bot.send_message(message.chat.id, "Thinking...")

    try:
        positive, negative, width, height = api.send_prompt(model_name=prompt["model"], values=prompt["parameters"], natural_language=content, history=history)

        bot.edit_message_text(f"+ {positive}\n\n- {negative}\n\n{width}x{height}", msg.chat.id, msg.id)
    except Exception as e:
        bot.edit_message_text(f"Exception: {e}", msg.chat.id, msg.id)


    while len(history) > 20:
        history.pop(0)

def send_file_to_chat(file_name, file_path):
    try:
        chat_id = file_name.split('_')[0]
        if not chat_id.isdigit():
            return False, f"Некорректное имя файла: {file_name}"
        chat_id = int(chat_id)
        with open(file_path, 'rb') as img:
            bot.send_photo(chat_id, img)
        return True, f"Файл {file_name} отправлен пользователю {chat_id}."
    except Exception as e:
        return False, f"Ошибка отправки файла {file_name}: {e}"

def check_new_files():
    files = os.listdir(WATCH_FOLDER)
    for file_name in files:
        # Проверяем, является ли файл изображением
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            file_path = os.path.join(WATCH_FOLDER, file_name)
            # Отправляем файл пользователю
            result, log = send_file_to_chat(file_name, file_path)
            print(log)
            if result:
                os.rename(WATCH_FOLDER + "\\" + file_name, "sent\\" + str(randint(0, 10 ** 16)) + file_name)
            

def monitor_folder():
    while True:
        check_new_files()
        time.sleep(1)