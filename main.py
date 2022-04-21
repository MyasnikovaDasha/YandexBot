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

used_cities = []  # Переменные для работы игры "Города"
phrases = ["Принято!", "Слышал что-то знакомое...", "Записал!", "Так значит? Ну держись тогда!", "Прекрасное местечко!",
           "Я бы хотел там оказаться...", "Ни за что туда не отправлюсь.", "Такой себе город, я бы там не жил.",
           "Засчитываю!",
           "И такой город бывает?", "Чего только люди не придумают..."]

music_list_classic = [
    ['Мелодия1.mp3', '/Bach', 'Toccata and Fugue in D minor', '/Glinka', '/Schubert', '/Chajjkovskijj'],
    ['Мелодия2.mp3', '/Betkhoven', 'lunnaja-sonata', '/Chopin', '/Vivaldi', '/Bach'],
    ['Мелодия3.mp3', '/Grig', 'per-gjunt-v-peshhere-gornogo-korolja', '/Mocart', '/Bach', '/Glinka'],
    ['Мелодия4.mp3', '/Glinka', 'Marsh_Chernomora', '/Vivaldi', '/Schubert', '/Chajjkovskijj'],
    ['Мелодия5.mp3', '/Mocart', 'zhenitba-figaro', '/Chajjkovskijj', '/Bach', '/Chopin'],
    ['Мелодия6.mp3', '/Mocart', 'Piano Sonata 11 A', '/Chopin', '/Betkhoven', '/Grig'],
    ['Мелодия7.mp3', '/Chajjkovskijj', 'shhelkunchik-vals-cvetov', '/Mocart', '/Bach', '/Glinka'],
    ['Мелодия8.mp3', '/Chajjkovskijj', 'Tanec_malenkikh_lebedejj_iz_baleta_Lebedinoe_ozero',
     '/Vivaldi', '/Schubert', '/Bach'],
    ['Мелодия9.mp3', '/Vivaldi', 'vremena-goda-vesna', '/Betkhoven', '/Mocart',
     '/Grig']]  # список мелодий для игры в викторину: музыка, классика

music_list_contemporary = [['Песня1.mp3', '/Konfuz', '/Egor_Creed', '/Slava_Marlow', '/Timati'],
                           ['Песня2.mp3', '/Alex_Ataman', '/Feduk', '/Morgenshtern', '/Mucca'],
                           ['Песня3.mp3', '/Jony', '/Egor_Creed', '/Feduk', '/Danya_Milokhin'],
                           ['Песня4.mp3', '/Klava_Koka', '/Mia_Boyko', '/Dora', '/Polina_Gagarina'],
                           ['Песня5.mp3', '/Femlove', '/King_and_the_Clown', '/Mucca', 'Danya_Milokhin'],
                           ['Песня6.mp3', '/Artur_Pirozhkov', '/Khabib', '/Morgenshtern', '/Eldar_Dzharakhov'],
                           ['Песня7.mp3', '/Dabro', '/Egor_Creed', '/Eldar_Dzharakhov', '/Danya_Milokhin'],
                           ['Песня8.mp3', '/Billie_Eilish', '/Ariana_Grande', '/Selena_Gomez', '/Taylor_Swift'],
                           ['Песня9.mp3', '/BTS', '/EXO', '/XXXTENTACION', '/Kanye_West'],
                           ['Песня10.mp3', '/DEAD_BLONDE', '/Mia_Boyko', '/Maby_Baby', '/Alena_Shvets'],
                           ['Песня11.mp3', '/Nervy', '/King_and_the_Clown', '/friend_zone',
                            '/Timati']]  # список мелодий для игры в викторину: музыка, современная

art_list = [['Картина1.jpg', '/DIEGO_VELAZQUEZ', '/SANDRO_BOTTICELLI', '/PABLO_PICASSO', '/RAFAEL_SANTI'],
            ['Картина2.jpg', '/VINCENT_VAN_GOGH', '/PABLO_PICASSO', '/MICHELANGELO_CARAVAGGIO', '/EUGENE_DELACROIX'],
            ['Картина3.jpg', '/EDWARD_MUNK', '/SANDRO_BOTTICELLI', '/MICHELANGELO_CARAVAGGIO', '/JACKSON_POLLOCK'],
            ['Картина4.jpg', '/SALVADOR_DALI', '/PABLO_PICASSO', '/JACKSON_POLLOCK', '/JEROME_BOSCH'],
            ['Картина5.jpg', '/OREST_KIPRENSKY', '/SANDRO_BOTTICELLI', '/KAZIMIR_MALEVICH', '/JEROME_BOSCH'],
            ['Картина6.jpg', '/REMBRANDT_VAN_RHINE', '/RAFAEL_SANTI', '/MICHELANGELO_CARAVAGGIO', '/JEROME_BOSCH'],
            ['Картина7.jpg', '/BANKSY', '/SANDRO_BOTTICELLI', '/KAZIMIR_MALEVICH', '/JEROME_BOSCH'],
            ['Картина8.jpg', '/LEONARDO_DA_VINCI', '/RAFAEL_SANTI', '/JACKSON_POLLOCK', '/EUGENE_DELACROIX'],
            ['Картина9.jpg', '/CLAUDE_MONET', '/PABLO_PICASSO', '/KAZIMIR_MALEVICH',
             '/EUGENE_DELACROIX']]  # список картин для игры в викторину искусство

films_list = [
    ['Фильм1.jpg', '/Krik', '/Pyatnitsa_13', '/Krovavoye_leto', '/Tretiy_Lishniy'],
    ['Фильм2.jpg', '/Tachki', '/Gonka_Pushechnoye_yadro', '/Avtomobili', '/Beregis_avtomobilya'],
    ['Фильм3.jpg', '/Kavkazskaya_plennitsa', '/Ironiya_Sudby_ili_s_logkim_parom',
     '/Afonya', '/Dozhivem_do_ponedelnika'],
    ['Фильм4.jpg', '/Sudya_Dredd', '/Razrushitel', '/Kobra', '/Politseyskiy_bespredel'],
    ['Фильм5.jpg', '/Titanik', '/1912', '/Kapitan_Kryuk', '/Romeo_Dzhulyetta'],
    ['Фильм6.jpg', '/Angely_Charli', '/Komanda_A', '/8_Podrug_Oushena', '/Operatsiya_Argo'],
    ['Фильм7.jpg', '/Office', '/Biezumcy', '/Kak_ya_vstretil_vashu_mamu', '/Malkolm_v_tsentre_vnimaniya'],
    ['Фильм8.jpg', '/Alexander', '/Troya', '/Bogi_i_Monstry', '/Gladiator'],
    ['Фильм9.jpg', '/Amerikanskiy_Pirog', '/Euro_Tour', '/Super_Pertsy', '/Tretiy_Lishniy'],
    ['Фильм10.jpg', '/Brat', '/Den_rozhdeniya_Burzhuya', '/Boomer', '/Brigada'],
    ['Фильм11.jpg', '/Lyudi_v_chornom_2', '/Lyudi_v_chornom', '/Lyudi_v_chornom_interneshnl', '/Lyudi_v_chornom_3'],
    ['Фильм12.jpg', '/Den_Surka', '/Pomni', '/Bolshoy',
     '/Novaya_rozhdestvenskaya_istoriya']]  # список картин для игры в викторину фильмы

music_list_classic_new = music_list_classic  # для игры в викторину: музыка
music_list_contemporary_new = music_list_contemporary
ans_music = ''

art_list_new = art_list  # для игры в викторину: искусство
ans_art = ''

films_list_new = films_list
ans_film = ''

nomer = 0
points = 0


def start(update, context):  # приветствие пользователя
    user_name = update.message.chat.first_name
    update.message.reply_text(f"Привет, {user_name} 😊")
    reply_keyboard = [['/skills']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Меня зовут Словесный бот", reply_markup=markup)


def skills(update, context):  # навыки бота
    reply_keyboard = [['/play', '/rules']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = '\n'.join(["✅ /play - выбрать и сыграть с ботом в словесную игру", "✅ /rules - правила игры"])
    update.message.reply_text(text, reply_markup=markup)


def play(update, context):  # выбор игры
    reply_keyboard = [['/goroda', '/quiz']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('В какую игру ты хочешь сыграть?', reply_markup=markup)


def rules(update, context):  # ---Правила игры--- # ИСПРАВИТЬ
    reply_keyboard = [['/play', ]]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = '\n'.join(["✅ /play - выбрать и сыграть с ботом в словесную игру",
                      "✅ /rules - правила игры"])
    update.message.reply_text(text, reply_markup=markup)


def quiz(update, context):  # игра - викторина
    reply_keyboard = [['/movie'], ['/art', '/music']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('В какую викторину вы хотите сыграть?', reply_markup=markup)


def music(update, context):  # викторина, музыка
    global music_list_classic_new, nomer, points, music_list_contemporary_new
    nomer = 0
    points = 0
    random.shuffle(music_list_classic, random.random)
    music_list_classic_new = music_list_classic
    random.shuffle(music_list_contemporary, random.random)
    music_list_contemporary_new = music_list_contemporary
    reply_keyboard = [['/contemporary', '/classic']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Выберите тему', reply_markup=markup)


def classic(update, context):  # викторина, музыка
    global ans_music, nomer
    if nomer != 5:
        options = [music_list_classic_new[nomer][1], music_list_classic_new[nomer][-1],
                   music_list_classic_new[nomer][-2], music_list_classic_new[nomer][-3]]
        ans_music = options[0][::]
        random.shuffle(options, random.random)
        reply_keyboard = [[options[0], options[1]], [options[2], options[3]]]  # кнопка
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        chat_id = update.message.chat.id
        meleodia = music_list_classic_new[nomer][0]
        nomer += 1
        context.bot.send_audio(chat_id=chat_id, audio=open(meleodia, 'rb'))
        update.message.reply_text('Выберите композитора', reply_markup=markup)
    else:
        text = 'Ваш результат: ' + str(points) + ' из 5'
        update.message.reply_text(text)


def contemporary(update, context):  # викторина, музыка
    global ans_music, nomer
    if nomer != 5:
        options = [music_list_contemporary_new[nomer][1], music_list_contemporary_new[nomer][-1],
                   music_list_contemporary_new[nomer][-2], music_list_contemporary_new[nomer][-3]]
        ans_music = options[0][::]
        random.shuffle(options, random.random)
        reply_keyboard = [[options[0], options[1]], [options[2], options[3]]]  # кнопка
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        chat_id = update.message.chat.id
        meleodia = music_list_contemporary_new[nomer][0]
        nomer += 1
        context.bot.send_audio(chat_id=chat_id, audio=open(meleodia, 'rb'))
        update.message.reply_text('Выберите исполнителя', reply_markup=markup)
    else:
        text = 'Ваш результат: ' + str(points) + ' из 5'
        update.message.reply_text(text)


def music_check_mistake(update, context):
    global points
    reply_keyboard = [['/next_contemporary']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = 'Правильный ответ: ' + ans_music[1:]
    update.message.reply_text(text, reply_markup=markup)


def music_check_right(update, context):
    global points
    reply_keyboard = [['/next_contemporary']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Правильно', reply_markup=markup)
    points += 1


def art(update, context):  # викторина, картины
    global art_list, nomer, points, art_list_new
    nomer = 0
    points = 0
    random.shuffle(art_list, random.random)
    art_list_new = art_list
    reply_keyboard = [['/next_art']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Удачи)', reply_markup=markup)


def next_art(update, context):  # викторина, музыка
    global ans_art, nomer
    if nomer != 5:
        options = [art_list_new[nomer][1], art_list_new[nomer][-1],
                   art_list_new[nomer][-2], art_list_new[nomer][-3]]
        ans_art = options[0][::]
        random.shuffle(options, random.random)
        reply_keyboard = [[options[0], options[1]], [options[2], options[3]]]  # кнопка
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        chat_id = update.message.chat.id
        picture = art_list_new[nomer][0]
        nomer += 1
        context.bot.send_photo(chat_id=chat_id, photo=open(picture, 'rb'))
        update.message.reply_text('Выберите художника', reply_markup=markup)
    else:
        text = 'Ваш результат: ' + str(points) + ' из 5'
        update.message.reply_text(text)


def paintings_check_mistake(update, context):
    global points
    reply_keyboard = [['/next_art']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = 'Правильный ответ: ' + ans_art[1:]
    update.message.reply_text(text, reply_markup=markup)


def paintings_check_right(update, context):
    global points
    reply_keyboard = [['/next_art']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Правильно', reply_markup=markup)
    points += 1

def movie(update, context):  # викторина, картины
    global films_list, nomer, points, films_list_new
    nomer = 0
    points = 0
    random.shuffle(films_list, random.random)
    films_list_new = films_list
    reply_keyboard = [['/next_movie']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Удачи)', reply_markup=markup)


def next_movie(update, context):  # викторина, музыка
    global ans_film, nomer
    if nomer != 5:
        options = [films_list_new[nomer][1], films_list_new[nomer][-1],
                   films_list_new[nomer][-2], films_list_new[nomer][-3]]
        ans_film = options[0][::]
        random.shuffle(options, random.random)
        reply_keyboard = [[options[0], options[1]], [options[2], options[3]]]  # кнопка
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        chat_id = update.message.chat.id
        picture = films_list_new[nomer][0]
        nomer += 1
        context.bot.send_photo(chat_id=chat_id, photo=open(picture, 'rb'))
        update.message.reply_text('Выберите название фильма', reply_markup=markup)
    else:
        text = 'Ваш результат: ' + str(points) + ' из 5'
        update.message.reply_text(text)


def logics_check_mistake(update, context):
    global points
    reply_keyboard = [['/next_movie']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    text = 'Правильный ответ: ' + ans_film[1:]
    update.message.reply_text(text, reply_markup=markup)


def logics_check_right(update, context):
    global points
    reply_keyboard = [['/next_movie']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Правильно', reply_markup=markup)
    points += 1

def bach(update, context):  # Функции для викторины: музыка, классика
    global points
    reply_keyboard = [['/next_classic']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if ans_music == '/Bach':
        update.message.reply_text('Правильно', reply_markup=markup)
        points += 1
    else:
        text = 'Правильный ответ: ' + ans_music[1:]
        update.message.reply_text(text, reply_markup=markup)


def glinka(update, context):  # Функции для викторины: музыка, классика
    global points
    reply_keyboard = [['/next_classic']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if ans_music == '/Glinka':
        update.message.reply_text('Правильно', reply_markup=markup)
        points += 1
    else:
        text = 'Правильный ответ: ' + ans_music[1:]
        update.message.reply_text(text, reply_markup=markup)


def schubert(update, context):  # Функции для викторины: музыка, классика
    global points
    reply_keyboard = [['/next_classic']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if ans_music == '/Schubert':
        update.message.reply_text('Правильно', reply_markup=markup)
        points += 1
    else:
        text = 'Правильный ответ: ' + ans_music[1:]
        update.message.reply_text(text, reply_markup=markup)


def chajjkovskijj(update, context):  # Функции для викторины: музыка, классика
    global points
    reply_keyboard = [['/next_classic']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if ans_music == '/Chajjkovskijj':
        update.message.reply_text('Правильно', reply_markup=markup)
        points += 1
    else:
        text = 'Правильный ответ: ' + ans_music[1:]
        update.message.reply_text(text, reply_markup=markup)


def betkhoven(update, context):  # Функции для викторины: музыка, классика
    global points
    reply_keyboard = [['/next_classic']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if ans_music == '/Betkhoven':
        update.message.reply_text('Правильно', reply_markup=markup)
        points += 1
    else:
        text = 'Правильный ответ: ' + ans_music[1:]
        update.message.reply_text(text, reply_markup=markup)


def chopin(update, context):  # Функции для викторины: музыка, классика
    global points
    reply_keyboard = [['/next_classic']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if ans_music == '/Chopin':
        update.message.reply_text('Правильно', reply_markup=markup)
        points += 1
    else:
        text = 'Правильный ответ: ' + ans_music[1:]
        update.message.reply_text(text, reply_markup=markup)


def vivaldi(update, context):  # Функции для викторины: музыка, классика
    global points
    reply_keyboard = [['/next_classic']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if ans_music == '/Vivaldi':
        update.message.reply_text('Правильно', reply_markup=markup)
        points += 1
    else:
        text = 'Правильный ответ: ' + ans_music[1:]
        update.message.reply_text(text, reply_markup=markup)


def grig(update, context):  # Функции для викторины: музыка, классика
    global points
    reply_keyboard = [['/next_classic']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if ans_music == '/Grig':
        update.message.reply_text('Правильно', reply_markup=markup)
        points += 1
    else:
        text = 'Правильный ответ: ' + ans_music[1:]
        update.message.reply_text(text, reply_markup=markup)


def mocart(update, context):  # Функции для викторины: музыка, классика
    global points
    reply_keyboard = [['/next_classic']]  # кнопка
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if ans_music == '/Mocart':
        update.message.reply_text('Правильно', reply_markup=markup)
        points += 1
    else:
        text = 'Правильный ответ: ' + ans_music[1:]
        update.message.reply_text(text, reply_markup=markup)


def start_goroda(update, context):  # игра - города
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

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("skills", skills))
    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("quiz", quiz))

    dp.add_handler(CommandHandler("music", music))
    dp.add_handler(CommandHandler("classic", classic))
    dp.add_handler(CommandHandler("next_classic", classic))
    dp.add_handler(CommandHandler("next_contemporary", contemporary))
    dp.add_handler(CommandHandler("contemporary", contemporary))
    dp.add_handler(CommandHandler("art", art))
    dp.add_handler(CommandHandler("next_art", next_art))
    dp.add_handler(CommandHandler("movie", movie))
    dp.add_handler(CommandHandler("next_movie", next_movie))

    dp.add_handler(CommandHandler("Bach", bach))
    dp.add_handler(CommandHandler("Glinka", glinka))
    dp.add_handler(CommandHandler("Schubert", schubert))
    dp.add_handler(CommandHandler("Chajjkovskijj", chajjkovskijj))
    dp.add_handler(CommandHandler("Betkhoven", betkhoven))
    dp.add_handler(CommandHandler("Chopin", chopin))
    dp.add_handler(CommandHandler("Vivaldi", vivaldi))
    dp.add_handler(CommandHandler("Grig", grig))
    dp.add_handler(CommandHandler("Mocart", mocart))

    dp.add_handler(CommandHandler("Konfuz", music_check_right))
    dp.add_handler(CommandHandler("Alex_Ataman", music_check_right))
    dp.add_handler(CommandHandler("Jony", music_check_right))
    dp.add_handler(CommandHandler("Klava_Koka", music_check_right))
    dp.add_handler(CommandHandler("Femlove", music_check_right))
    dp.add_handler(CommandHandler("Artur_Pirozhkov", music_check_right))
    dp.add_handler(CommandHandler("Billie_Eilish", music_check_right))
    dp.add_handler(CommandHandler("DEAD_BLONDE", music_check_right))
    dp.add_handler(CommandHandler("BTS", music_check_right))
    dp.add_handler(CommandHandler("Dabro", music_check_right))
    dp.add_handler(CommandHandler("Nervy", music_check_right))

    dp.add_handler(CommandHandler("Ariana_Grande", music_check_mistake))
    dp.add_handler(CommandHandler("Mia_Boyko", music_check_mistake))
    dp.add_handler(CommandHandler("Selena_Gomez", music_check_mistake))
    dp.add_handler(CommandHandler("Taylor_Swift", music_check_mistake))
    dp.add_handler(CommandHandler("Maby_Baby", music_check_mistake))
    dp.add_handler(CommandHandler("Alena_Shvets", music_check_mistake))
    dp.add_handler(CommandHandler("Dora", music_check_mistake))
    dp.add_handler(CommandHandler("Polina_Gagarina", music_check_mistake))
    dp.add_handler(CommandHandler("Egor_Creed", music_check_mistake))
    dp.add_handler(CommandHandler("King_and_the_Clown", music_check_mistake))
    dp.add_handler(CommandHandler("EXO", music_check_mistake))
    dp.add_handler(CommandHandler("XXXTENTACION", music_check_mistake))
    dp.add_handler(CommandHandler("Kanye_West", music_check_mistake))
    dp.add_handler(CommandHandler("friend_zone", music_check_mistake))
    dp.add_handler(CommandHandler("Feduk", music_check_mistake))
    dp.add_handler(CommandHandler("Slava_Marlow", music_check_mistake))
    dp.add_handler(CommandHandler("Khabib", music_check_mistake))
    dp.add_handler(CommandHandler("Timati", music_check_mistake))
    dp.add_handler(CommandHandler("Mucca", music_check_mistake))
    dp.add_handler(CommandHandler("Eldar_Dzharakhov", music_check_mistake))
    dp.add_handler(CommandHandler("Morgenshtern", music_check_mistake))
    dp.add_handler(CommandHandler("Danya_Milokhin", music_check_mistake))

    dp.add_handler(CommandHandler("DIEGO_VELAZQUEZ", paintings_check_right))
    dp.add_handler(CommandHandler("VINCENT_VAN_GOGH", paintings_check_right))
    dp.add_handler(CommandHandler("EDWARD_MUNK", paintings_check_right))
    dp.add_handler(CommandHandler("SALVADOR_DALI", paintings_check_right))
    dp.add_handler(CommandHandler("OREST_KIPRENSKY", paintings_check_right))
    dp.add_handler(CommandHandler("REMBRANDT_VAN_RHINE", paintings_check_right))
    dp.add_handler(CommandHandler("BANKSY", paintings_check_right))
    dp.add_handler(CommandHandler("LEONARDO_DA_VINCI", paintings_check_right))
    dp.add_handler(CommandHandler("CLAUDE_MONET", paintings_check_right))

    dp.add_handler(CommandHandler("SANDRO_BOTTICELLI", paintings_check_mistake))
    dp.add_handler(CommandHandler("PABLO_PICASSO", paintings_check_mistake))
    dp.add_handler(CommandHandler("RAFAEL_SANTI", paintings_check_mistake))
    dp.add_handler(CommandHandler("MICHELANGELO_CARAVAGGIO", paintings_check_mistake))
    dp.add_handler(CommandHandler("KAZIMIR_MALEVICH", paintings_check_mistake))
    dp.add_handler(CommandHandler("JACKSON_POLLOCK", paintings_check_mistake))
    dp.add_handler(CommandHandler("EUGENE_DELACROIX", paintings_check_mistake))
    dp.add_handler(CommandHandler("JEROME_BOSCH", paintings_check_mistake))

    dp.add_handler(CommandHandler("Krik", logics_check_right))
    dp.add_handler(CommandHandler("Tachki", logics_check_right))
    dp.add_handler(CommandHandler("Kavkazskaya_plennitsa", logics_check_right))
    dp.add_handler(CommandHandler("Dozhivem_do_ponedelnika", logics_check_right))
    dp.add_handler(CommandHandler("Titanik", logics_check_right))
    dp.add_handler(CommandHandler("Sudya_Dredd", logics_check_right))
    dp.add_handler(CommandHandler("Angely_Charli", logics_check_right))
    dp.add_handler(CommandHandler("Office", logics_check_right))
    dp.add_handler(CommandHandler("Alexander", logics_check_right))
    dp.add_handler(CommandHandler("Amerikanskiy_Pirog", logics_check_right))
    dp.add_handler(CommandHandler("Brat", logics_check_right))
    dp.add_handler(CommandHandler("Lyudi_v_chornom_2", logics_check_right))
    dp.add_handler(CommandHandler("Den_Surka", logics_check_right))

    dp.add_handler(CommandHandler("Pyatnitsa_13", logics_check_mistake))
    dp.add_handler(CommandHandler("Krovavoye_leto", logics_check_mistake))
    dp.add_handler(CommandHandler("Gonka_Pushechnoye_yadro", logics_check_mistake))
    dp.add_handler(CommandHandler("Avtomobili", logics_check_mistake))
    dp.add_handler(CommandHandler("Beregis_avtomobilya", logics_check_mistake))
    dp.add_handler(CommandHandler("Ironiya_Sudby_ili_s_logkim_parom", logics_check_mistake))
    dp.add_handler(CommandHandler("Afonya", logics_check_mistake))
    dp.add_handler(CommandHandler("Kobra", logics_check_mistake))
    dp.add_handler(CommandHandler("Razrushitel", logics_check_mistake))
    dp.add_handler(CommandHandler("Politseyskiy_bespredel", logics_check_mistake))
    dp.add_handler(CommandHandler("1912", logics_check_mistake))
    dp.add_handler(CommandHandler("Kapitan_Kryuk", logics_check_mistake))
    dp.add_handler(CommandHandler("Romeo_Dzhulyetta", logics_check_mistake))
    dp.add_handler(CommandHandler("Komanda_A", logics_check_mistake))
    dp.add_handler(CommandHandler("8_Podrug_Oushena", logics_check_mistake))
    dp.add_handler(CommandHandler("Operatsiya_Argo", logics_check_mistake))
    dp.add_handler(CommandHandler("Biezumcy", logics_check_mistake))
    dp.add_handler(CommandHandler("Kak_ya_vstretil_vashu_mamu", logics_check_mistake))
    dp.add_handler(CommandHandler("Malkolm_v_tsentre_vnimaniya", logics_check_mistake))
    dp.add_handler(CommandHandler("Troya", logics_check_mistake))
    dp.add_handler(CommandHandler("Bogi_i_Monstry", logics_check_mistake))
    dp.add_handler(CommandHandler("Gladiator", logics_check_mistake))
    dp.add_handler(CommandHandler("Euro_Tour", logics_check_mistake))
    dp.add_handler(CommandHandler("Super_Pertsy", logics_check_mistake))
    dp.add_handler(CommandHandler("Tretiy_Lishniy", logics_check_mistake))
    dp.add_handler(CommandHandler("Den_rozhdeniya_Burzhuya", logics_check_mistake))
    dp.add_handler(CommandHandler("Boomer", logics_check_mistake))
    dp.add_handler(CommandHandler("Brigada", logics_check_mistake))
    dp.add_handler(CommandHandler("Lyudi_v_chornom", logics_check_mistake))
    dp.add_handler(CommandHandler("Lyudi_v_chornom_interneshnl", logics_check_mistake))
    dp.add_handler(CommandHandler("Lyudi_v_chornom_3", logics_check_mistake))
    dp.add_handler(CommandHandler("Pomni", logics_check_mistake))
    dp.add_handler(CommandHandler("Bolshoy", logics_check_mistake))
    dp.add_handler(CommandHandler("Novaya_rozhdestvenskaya_istoriya", logics_check_mistake))

    dp.add_handler(conv_handler_goroda)

    updater.start_polling()  # Запускаем цикл приема и обработки сообщений.
    updater.idle()  # Ждём завершения приложения. # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)


if __name__ == '__main__':  # Запускаем функцию main() в случае запуска скрипта.
    main()
