import api
import telebot
import prompt_handler

token = open("bot_token.txt", "r").read()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['txt2img'])
def txt2img(message: telebot.telebot.types.Message):
    content = message.text

    prompt = prompt_handler.txt2prompt(content)

    api.send_prompt(model_name=prompt["model"], values=prompt["parameters"])