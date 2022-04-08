# Импортируем необходимые классы.
# САМ БОТ ЗДЕСЬ: http://t.me/YLWordBot
import logging
import json
import random
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5296394501:AAEjbMymwTSV-nQCCHbLsNBlIvvDvszRGl4'

# Городов всего: 10969
with open('cities.json', encoding="utf-8") as city_file:
    city_data = json.load(city_file)
print(len(city_data["city"]))


def goroda(update, context):
    update.message.reply_text(city_data["city"][random.randint(0, 10969)]["name"])


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(TOKEN)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("goroda", goroda))
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()