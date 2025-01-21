import bot
import threading

def main():
    folder_thread = threading.Thread(target=bot.monitor_folder)
    folder_thread.daemon = True
    folder_thread.start()
    bot.bot.infinity_polling()

if __name__ == "__main__":
    main()