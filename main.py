# Импортируем необходимые классы.
# САМ БОТ ЗДЕСЬ: http://t.me/YLWordBot
import logging
import json
import random
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler,ConversationHandler

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5296394501:AAEjbMymwTSV-nQCCHbLsNBlIvvDvszRGl4'

# Городов всего: 10969
with open('sorted_cities.json', encoding="utf-8") as city_file:
    city_data = json.load(city_file)

used_cities = []


def start_goroda(update, context):
    update.message.reply_text("Приветствую в игре города! Напиши \'Go\', если хочешь, чтоб мы начали. В любое время напиши /stop и мы закончим игру")
    return 1


def sure(update, context):
    ans = update.message.text
    if ans.lower().capitalize() == "Go":
        temp = list(city_data.keys())
        temp = random.choice(temp)
        temp = city_data[temp]
        word = random.choice(temp)
        used_cities.append(word)
        update.message.reply_text(f'Отлично. Я начну. Мой город: {word}')
        return 2
    update.message.reply_text('Не понял тебя. Повтори, пожалуйста.')
    return 1


def goroda_player_turn(update, context):
    word = update.message.text
    word = ' '.join([i.lower().capitalize() for i in word.split()])
    word = '-'.join([i.lower().capitalize() for i in word.split('-')])
    word = word.replace('ё', 'e')
    word = word.replace('Ё', 'Е')
    try:
        first_key_words = city_data[word[0].upper()]
        if word in used_cities:
            update.message.reply_text(f'Город {word} уже упоминался. Давай ещё раз и не повторяйся!')
            raise KeyError
        if word not in first_key_words:
            update.message.reply_text('Нет в словаре')
            print(word)
            print(first_key_words)
            raise KeyError
        if not(used_cities[-1][-1] == word[0].lower() or
                used_cities[-1][-2] == word[0].lower() and used_cities[-1][-1].lower() in 'ъыь'):
            update.message.reply_text('Не совпадает с буквой')
            raise KeyError
        used_cities.append(word)
        print(used_cities)
        word = goroda_computer_turn()
        update.message.reply_text(f'Принято! Мой город: {word}')
        return 2
    except KeyError:
        return 2


def goroda_computer_turn():
    next_key = used_cities[-1][-1].capitalize()
    if next_key in 'ЪЫЬ':
        next_key = used_cities[-1][-2].capitalize()
    word = random.choice(city_data[next_key])
    while word in used_cities:
        print(' застрял')
        word = random.choice(city_data[next_key])
    used_cities.append(word)
    return word


def stop(update, context):
    update.message.reply_text("Принято! Интересно поиграли!")
    used_cities.clear()
    return ConversationHandler.END


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(TOKEN)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        entry_points=[CommandHandler('goroda', start_goroda)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, sure)],
            2: [MessageHandler(Filters.text & ~Filters.command, goroda_player_turn)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()