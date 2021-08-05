import telebot
from telebot import types

token = "1932220619:AAEyCbHdomHt1a8geevbZCgOEyXbDKwpToc"

bot = telebot.TeleBot(token)

questions = [
    ("Что такое экология?", "Защита природы."),
    ("Что такое загрязнение?", "Это загрязнение природы."),
    ("Из-за чего происходит эрозия почвы?", "Выбросы химии в почву."),
    ("Из-за чего происходит радиоактивное загрязнение?", "Сбоев в атом. электростанций."),
    ("Что такое термическое загрязнение?", "Ухудшение качества воды."),
    ("Что такое антропогенное загрязнение?", "Воздействие на окруж. среду."),
]

options = [
    ("Интернет компания.", "Защита природы.", "Выращивание растений.", "Помощь бездомным животным."),
    ("Это загрязнение природы.", "Суботники", "Это частые дожди,и ливни.", "Истребление животных."),
    ("Выбросы химии в почву.", "Когда её топтут животные.", "Когда на ней растут леса.", "За ней не ухаживают."),
    ("Из-за сбоев микрофона.", "Из-за машин.", "Сбоев в атом. электростанций.", "Из-за поломок станций."),
    ("Это заростение водорослей.", "Ухудшение качества воды.", "Это смена цвета воды.", "Тех. поподающая в воды."),
    ("Воздействие на окруж. среду.", "Уход за скотом.", "Много играть в ПК.", "Строительство домов."),
]  

state = 0
countSuccess = 0
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.text == "/start":
        keyboard = types.InlineKeyboardMarkup()
        text = """Если вы считаете что смогли бы ответить на все мои вопросы связанные с экологией, выберите кнопку "Ответить на вопросы", однако если у вас есть сомнения насчет этого,
выберите кнопку "Прочитать теория", после чего, вы сможете прочитать немного про экологию, узнать 
какие проблемы связанные с экологией есть в Чеченской республике, и главное принять тот факт, что если 
мы хотим чтобы у нас экология была лучше чем во всех других регионах России, надо начать с себя. 
Остальное на сайте)
    """
        btnQuiz = types.InlineKeyboardButton(
            "Начать викторину", callback_data="Quiz")
        btnSite = types.InlineKeyboardButton(
            "Перейти на сайт", url="https://ecologychr.herokuapp.com/")
        keyboard.add(btnQuiz, btnSite, row_width=2)
        bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def start_callback(call):  
    global state, countSuccess
    if call.message:
        if call.data == "Quiz":
            state = 0
            countSuccess = 0
            bot.send_message(call.message.chat.id, "И так, ты решил пройти викторину. Чтож, добро пожаловать")
            start_quiz(call.message)
        else:
            if call.data == questions[state][1]:
                countSuccess += 1
            state += 1
            
            
            bot.delete_message(call.message.chat.id, call.message.id)
            start_quiz(call.message)

def start_quiz(message):
    global state
    global countSuccess
    
    if state < len(questions):
        keyboard = types.InlineKeyboardMarkup()
        for option in options[state]:
            keyboard.add(types.InlineKeyboardButton(str(option), callback_data=str(option)))
        question = questions[state][0]

        bot.send_message(message.chat.id, question, reply_markup=keyboard)
    else:
        if countSuccess <= 3:            
            bot.send_message(message.chat.id, f"Ты отгадал {countSuccess}/{len(questions)}.\n Извини,но ты проиграл попробуй ещё раз! ")
        else:
            bot.send_message(message.chat.id, f"Ты отгадал {countSuccess}/{len(questions)}.\nПоздравляем, ты прошел викторину, желаем тебе всего наилучшего. Можешь посоветовать друзьям пройти викторину, чтобы и они знали про экологию)")



bot.polling()
