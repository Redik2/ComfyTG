import bot
import threading

def main():
    print('starting')
    folder_thread = threading.Thread(target=bot.monitor_folder)
    folder_thread.daemon = True
    folder_thread.start()
    print('bot starting')
    bot.bot.infinity_polling()

if __name__ == "__main__":
    main()