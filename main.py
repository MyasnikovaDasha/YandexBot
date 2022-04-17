# САМ БОТ ЗДЕСЬ: http://t.me/YLWordBot
import logging  # Импортируем необходимые классы.
import json
import random
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)  # Запускаем логгирование

logger = logging.getLogger(__name__)

TOKEN = '5296394501:AAEjbMymwTSV-nQCCHbLsNBlIvvDvszRGl4'

with open('sorted_cities.json', encoding="utf-8") as city_file:  # Городов всего: 10969
    city_data = json.load(city_file)

# Переменные для работы игры "Города"
used_cities = []
phrases = ["Принято!", "Слышал что-то знакомое...", "Записал!", "Так значит? Ну держись тогда!", "Прекрасное местечко!",
           "Я бы хотел там оказаться...", "Ни за что туда не отправлюсь.", "Такой себе город, я бы там не жил.", "Засчитываю!",
           "И такой город бывает?", "Чего только люди не придумают..."]

def start(update, context):  # приветствие пользователя
    user_name = update.message.chat.first_name
    update.message.reply_text(f"Привет, {user_name} 😊")
    reply_keyboard = [['/skills']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Меня зовут Словесный бот", reply_markup=markup)


def skills(update, context):
    reply_keyboard = [['/play', '/clear']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = '\n'.join(["✅ /play - выбрать и сыграть с ботом в словесную игру", "✅ /clear - удалить все сообщения"])
    update.message.reply_text(text, reply_markup=markup)


def play(update, context):
    reply_keyboard = [['/goroda', '/balabolka'], ['/quiz']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('В какую игру ты хочешь сыграть?', reply_markup=markup)


def clear(update, context): # ВАНЯ
    pass

#---НАЧАЛО КОДА НАД КОТОРЫМ РАБОТАЕТ ВАНЯ---


def start_balabolka(update, context):
    update.message.reply_text(
        "Приветствую в игре балаболка! Напиши \'Go\', если хочешь, "
        "чтоб мы начали. В любое время напиши /stop и мы закончим игру")
    return 1


def sure_balabolka(update, context):
    ans = update.message.text
    if ans.lower().capitalize() == "Go":
        print("Отлично! Начни печатать какое-либо предложение, и я на него сгенерирую текст. Затем ты продолжаешь и т.д.")
        return 2
    update.message.reply_text('Не понял тебя. Повтори, пожалуйста.')
    return 1


def balabolka_computer_turn(update, context):
    text = update.message.text
    pass


def start_goroda(update, context):
    update.message.reply_text(
        "Приветствую в игре города! Напиши \'Go\', если хочешь, "
        "чтоб мы начали. В любое время напиши /stop и мы закончим игру")
    return 1


def sure_goroda(update, context):
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
    word.replace("-На-", "-на-")
    word.replace("-Он-", '-он-')
    word = word.replace('ё', 'e')
    word = word.replace('Ё', 'Е')
    try:
        first_key_words = city_data[word[0].upper()]
        if word in used_cities:
            update.message.reply_text(f'Город {word} уже упоминался. Давай ещё раз и не повторяйся!')
            return 2
        if word not in first_key_words:
            update.message.reply_text('Нет в словаре')
            print(word)
            print(first_key_words)
            return 2
        if not (used_cities[-1][-1] == word[0].lower() or
                used_cities[-1][-2] == word[0].lower() and used_cities[-1][-1].lower() in 'ъыь'):
            update.message.reply_text('Не совпадает с буквой')
            return 2
        used_cities.append(word)
        print(used_cities)
        word = goroda_computer_turn()
        update.message.reply_text(f'{random.choice(phrases)} Мой город: {word}')
        return 2
    except KeyError:
        print("Такого города ЯВНО не существует")
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


def stop_goroda(update, context):
    update.message.reply_text("Принято! Интересно поиграли!")
    used_cities.clear()
    return ConversationHandler.END

#--- КОНЕЦ КОДА НАД КОТОРЫМ РАБОТАЕТ ВАНЯ ---


def main():
    updater = Updater(
        TOKEN)  # Создаём объект updater. # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен

    dp = updater.dispatcher  # Получаем из него диспетчер сообщений.

    conv_handler_goroda = ConversationHandler(
        entry_points=[CommandHandler('goroda', start_goroda)],  # Точка входа в диалог.
        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, sure_goroda)],
            2: [MessageHandler(Filters.text & ~Filters.command, goroda_player_turn)],
        },
        fallbacks=[CommandHandler('stop', stop_goroda)]  # Точка прерывания диалога. В данном случае — команда /stop.
    )

    conv_handler_balabolka = ConversationHandler(
        entry_points=[CommandHandler('balabolka', start_balabolka)],  # Точка входа в диалог.
        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, sure_balabolka)],
            2: [MessageHandler(Filters.text & ~Filters.command, balabolka_computer_turn)],
        },
        fallbacks=[CommandHandler('stop', stop_goroda)]  # Точка прерывания диалога. В данном случае — команда /stop.
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("skills", skills))
    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CommandHandler("clear", clear))
    dp.add_handler(conv_handler_goroda)
    dp.add_handler(conv_handler_balabolka)

    updater.start_polling()  # Запускаем цикл приема и обработки сообщений.
    updater.idle()  # Ждём завершения приложения. # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)


if __name__ == '__main__':  # Запускаем функцию main() в случае запуска скрипта.
    main()
