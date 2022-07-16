########################
# Project: LoveQuizBot #
# Developers:          #
# Naumov Dmitry        #
# Katkov Ilya          #
# Version: 1.1         #
# Platform: Telegram   #
# Language: Python     #
########################

# Modules
from typing import Type
import requests
import json
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
import sqlite3

# Settings
logging.basicConfig(level=logging.INFO)
bot = Bot(token="token")
dp = Dispatcher(bot)

connect = sqlite3.connect("base.db")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user1 VARCHAR(64) NULL,
    user2 VARCHAR(64) NULL,
    last_name VARCHAR(64) NULL,
    is_ready_user1 INTEGER(1),
    is_ready_user2 INTEGER(1),
    is_ready_game INTEGER(1)
    )
    """)

# Functions
def setLastName(last_name, user_id):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    cursor.execute("""UPDATE users SET last_name = ? WHERE user_id = ?""", [last_name, user_id])
    connect.commit()
    connect.close()

def getLastName(user_id):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    last_name_fetch = cursor.execute("""SELECT last_name FROM users WHERE user_id = ?""", [user_id])
    last_name = last_name_fetch.fetchone()[0]
    if last_name is None:
        return ""
    else:
        return last_name

# def addUser(user_id) - user_id = user_id, last_mes_time = time(), is_ready2 = 0, is_ready_game = 0
def addUser(user_id):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    is_ready_user2 = 0
    is_ready_game = 0
    cursor.execute("""INSERT INTO users (user_id, is_ready_user2, is_ready_game) VALUES (?, ?, ?)""", [user_id, is_ready_user2, is_ready_game])
    connect.commit()
    connect.close()

def isUser(user_id):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    is_user_fetch = cursor.execute("""SELECT user_id FROM users WHERE user_id = ?""", [user_id])
    is_user = is_user_fetch.fetchone()
    connect.close()
    try:
        if len(is_user) > 0:
            return True
    except TypeError:
        addUser(user_id)
        return True

def setUser1(user_id, user1_name):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    cursor.execute("""UPDATE users SET user1 = ? WHERE user_id = ?""", [user1_name, user_id])
    connect.commit()
    connect.close()

def setUser2(user_id, user2_name):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    cursor.execute("""UPDATE users SET user2 = ? WHERE user_id = ?""", [user2_name, user_id])
    connect.commit()
    connect.close()

def getUser1(user_id):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    get_user1_fetch = cursor.execute("""SELECT user1 FROM users WHERE user_id = ?""", [user_id])
    get_user1 = get_user1_fetch.fetchone()[0]
    if get_user1 is None:
        return ""
    else:
        return get_user1
        
def getUser2(user_id):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    get_user2_fetch = cursor.execute("""SELECT user2 FROM users WHERE user_id = ?""", [user_id])
    get_user2 = get_user2_fetch.fetchone()[0]
    if get_user2 is None:
        return ""
    else:
        return get_user2

def getIsReadyUser1(user_id):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    get_is_ready_user1_fetch = cursor.execute("""SELECT is_ready_user1 FROM users WHERE user_id = ?""", [user_id])
    get_is_ready_user1 = get_is_ready_user1_fetch.fetchone()[0]
    if get_is_ready_user1 is None:
        return ""
    else:
        return get_is_ready_user1
    
def getIsReadyUser2(user_id):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    get_is_ready_user2_fetch = cursor.execute("""SELECT is_ready_user2 FROM users WHERE user_id = ?""", [user_id])
    get_is_ready_user2 = get_is_ready_user2_fetch.fetchone()[0]
    if get_is_ready_user2 is None:
        return ""
    else:
        return get_is_ready_user2

def setIsReadyUser1(user_id, value):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    cursor.execute("""UPDATE users SET is_ready_user1 = ? WHERE user_id = ?""", [value, user_id])
    connect.commit()
    connect.close()

def setIsReadyUser2(user_id, value):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    cursor.execute("""UPDATE users SET is_ready_user2 = ? WHERE user_id = ?""", [value, user_id])
    connect.commit()
    connect.close()

def deleteUser(user_id):
    connect = sqlite3.connect("base.db")
    cursor = connect.cursor()
    cursor.execute("""DELETE FROM users WHERE user_id = ? """, [user_id])
    connect.commit()
    connect.close()

# Markups
btn_next = "Далее"
menu_start = ReplyKeyboardMarkup(resize_keyboard=True)
menu_start.add(btn_next)

btn_next_question = "Следующий вопрос"
btn_reset = "Начать заново"
menu_in_game = ReplyKeyboardMarkup(resize_keyboard=True)
menu_in_game.add(btn_next_question, btn_reset)

# Commands
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, "💕Буду задавать вопросы, которые помогут вам классно провести время и узнать друг друга поближе💕", reply_markup=menu_start)

@dp.message_handler()
async def bot_message(message: types.Message):
    user_id = message.from_user.id
    if isUser(user_id):
        if getIsReadyUser1(user_id) == 1:
            setUser1(user_id, message.text)
            setIsReadyUser1(user_id, 0)
            setLastName(message.text, user_id)
        if getIsReadyUser2(user_id) == 1:
            setUser2(user_id, message.text)
            setIsReadyUser2(user_id, 0)
        if getUser1(user_id) == "" or getIsReadyUser1(user_id) == "":
            setIsReadyUser1(user_id, 1)
            await bot.send_message(message.from_user.id, "Введите имя первого игрока: ", reply_markup=types.ReplyKeyboardRemove())
        elif getUser2(user_id) == "" or getIsReadyUser2(user_id) == "":
            setIsReadyUser2(user_id, 1)
            await bot.send_message(message.from_user.id, "Введите имя второго игрока: ")    
        else:
            last_name = getLastName(user_id)
            if last_name == getUser2(user_id):
                last_name = getUser1(user_id)
                setLastName(last_name, user_id)
            else:
                last_name = getUser2(user_id)
                setLastName(last_name, user_id)

        if message.text == "Начать заново":
            deleteUser(user_id)
            await bot.send_message(message.from_user.id, "Начинаем заново, введите два имени:", reply_markup=menu_start)  
        elif message.text == "Далее":
            pass
        else:
            response = requests.get("https://lovequiz.ru/api/getQuestion/").text.lower()
            data = json.JSONDecoder().decode(response)
            await bot.send_message(user_id, last_name.title() + ", " + data["question"], reply_markup=menu_in_game)

# Run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)