import telebot
from telebot import types 
import psycopg2


bot = telebot.TeleBot("7284393013:AAFEnQOQevxbfVY7e6ofca777zj1BdwLIDk")

def get_conn():    
    connection = psycopg2.connect(
                        database = "main", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)
    return connection


def close_con(conn,cur):
    conn.close()
    cur.close()


def create_user_table():
    conn=get_conn()
    cur=conn.cursor()
    try:
        cur.execute("""
            create table if not exists users(
            id varchar(120) primary key,
            first_name varchar(40) null,
            last_name varchar(30) null,
            telegram_account varchar(50) null
            )
            """)
        conn.commit()
        return "Table users created"
    except:
        return "users already exists"
    finally:
        close_con(conn,cur)


def add_user(id,first_name,last_name,telegram_account):
    conn=get_conn()
    cur=conn.cursor()
    try:
        cur.execute(f"""insert into users(id, first_name, last_name, telegram_account) values
                ('{id}', '{first_name}', '{last_name}', '{telegram_account}')""")
        
        conn.commit()

        return f"User with id {id} created"
    except Exception as ex:
        print(ex)
        return f"User with id{id} is already exists"
    finally:
        close_con(conn,cur)

admins = [5082812713]

def is_admin(user_id):
    return user_id in admins

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    create_user_table()
    add_user(message.chat.id,message.chat.first_name,message.chat.last_name,message.chat.username)
    if is_admin(user_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.InlineKeyboardButton("/help")
        btn2 = types.InlineKeyboardButton("/courses")
        markup.row(btn1, btn2) 
        bot.send_message(user_id, "Вы администратор!", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.InlineKeyboardButton("/help")
        btn2 = types.InlineKeyboardButton("/courses")
        markup.row(btn1, btn2) 
        bot.send_message(user_id, "Welcome to Soft Clab", reply_markup=markup)

@bot.message_handler(commands=['help'])
def helping(message):
    bot.send_message(message.chat.id, f"""
    Ин бот барои дохилшавии SoftClub мебошад.
    
    1.Ягон мушкили шид ба номерои +992*****7774 занг занед 
                     ташакур ба дикататон
                     барои малумоти бештар coursor ро зер кунед""")

@bot.message_handler(commands=['courses'])
def choose_course(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.InlineKeyboardButton("C++")
    btn2 = types.InlineKeyboardButton("HTML")
    btn3 = types.InlineKeyboardButton("JS")
    btn4 = types.InlineKeyboardButton("PYTHON")
    btn5 = types.InlineKeyboardButton("C#")
    btn6 = types.InlineKeyboardButton("REACT")
    btn7 = types.InlineKeyboardButton("Feedback")
    markup.row(btn1, btn2, btn3)
    markup.row(btn4, btn5, btn6)
    markup.row(btn7)

    bot.send_message(message.chat.id, "Привет! Выберите язык программирования:", reply_markup=markup)
    
@bot.message_handler(func=lambda message: True)
def handle_course(message):
    if message.text == "C++":
        bot.send_message(message.chat.id, 
                         """Учитель: Устод Курбонали;
Месячный Договор: 1000с;
Время Учебы: 16:00-18:00;
Start: 05.07.2024;
End: 05.08.2024;""")

    elif message.text == "HTML":
        bot.send_message(message.chat.id, 
                         """Учитель: Устод Мехриддин;
Месячный Договор: 1000с;
        Время Учебы: 18:00-20:00;
        Start: 05.07.2024;
        End: 05.08.2024;""")

    elif message.text == "JS":
        bot.send_message(message.chat.id, 
                         """Учитель: Устод Хасан;
        Месячный Договор: 1500с;
        Время Учебы: 18:00-20:00;
        Start: 05.07.2024;
        End: 05.08.2024;""")

    elif message.text == "PYTHON":
        bot.send_message(message.chat.id, 
                         """Учитель: Устод Хайриддин;
        Месячный Договор: 1500с;
        Время Учебы: 18:00-20:00;
        Start: 05.07.2024;
        End: 05.08.2024;""")

    elif message.text == "C#":
        bot.send_message(message.chat.id, 
                         """Учитель: Устод Аличон;
        Месячный Договор: 1500с;
        Время Учебы: 14:00-16:00;
        Start: 05.07.2024;
        End: 05.08.2024;""")

    elif message.text == "REACT":
        bot.send_message(message.chat.id, 
                         """Учитель: Устод Муин Гафуров;
        Месячный Договор: 1500с;
        Время Учебы: 18:00-20:00;
        Start: 05.07.2024;
        End: 05.08.2024;""")


def create_feedback_table():
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(100),
            feedback_text TEXT,
            submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (ID)
            );
        """)
        conn.commit()
    except Exception as e:
        print(f'Error creating feedback table: {str(e)}')
    finally:
        close_con(conn, cur)


def add_feedback(user_id, feedback_text):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO feedback (user_id, feedback_text) VALUES (%s, %s)
        """, (str(user_id), feedback_text))
        conn.commit()
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        close_con(conn, cur)

def ask_for_feedback(user_id):
    msg = bot.send_message(user_id, "Лутфан, фикру мулоҳизаҳои худро нависед:")
    bot.register_next_step_handler(msg, process_feedback)

def process_feedback(message):
    user_id = message.chat.id
    feedback_text = message.text
    add_feedback(user_id, feedback_text)
    bot.send_message(user_id, "Ташаккур барои фикру мулоҳизаҳоятон!")
    choose_course(message)

@bot.message_handler()
def handler(message):
    if  message.text == 'Feedback':
        ask_for_feedback(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'КАМАНДА ВУЧУТ НАДОРА')


bot.polling()