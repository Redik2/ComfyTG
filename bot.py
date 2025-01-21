import api
import telebot
import prompt_handler
from random import randint
from json import load

token = load(open("config.json", "r"))["token"]

bot = telebot.TeleBot(token)

sent_files = set()

WATCH_FOLDER = load(open("config.json", "r"))["output_folder"]

@bot.message_handler(commands=['txt2img'])
def txt2img(message: telebot.telebot.types.Message):
    content = message.text

    prompt = prompt_handler.txt2prompt(content)

    api.send_prompt(model_name=prompt["model"], values=prompt["parameters"])


def send_file_to_user(file_name, file_path):
    try:
        user_id = file_name.split('_')[0]
        if not user_id.isdigit():
            return f"Некорректное имя файла: {file_name}"
        user_id = int(user_id)
        with open(file_path, 'rb') as img:
            bot.send_photo(user_id, img, caption=str(randint(0, 999999)) + ".png")
        return f"Файл {file_name} отправлен пользователю {user_id}."
    except Exception as e:
        return f"Ошибка отправки файла {file_name}: {e}"

def check_new_files():
    global sent_files
    files = os.listdir(WATCH_FOLDER)
    for file_name in files:
        # Проверяем, является ли файл изображением
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            file_path = os.path.join(WATCH_FOLDER, file_name)
            # Проверяем, отправлялся ли этот файл ранее
            if file_name not in sent_files:
                # Отмечаем файл как отправленный
                sent_files.add(file_name)
                # Отправляем файл пользователю
                send_file_to_user(file_name, file_path)

def monitor_folder():
    while True:
        check_new_files()
        time.sleep(5)