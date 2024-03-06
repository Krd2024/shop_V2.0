import sqlite3
import telebot
from telebot import types
from src.wrapper_bot import TelegramBotWrapper
from src.utils import category
from decouple import config

TOKEN = config("TOKEN", cast=str, default="пусто")

bot = TelegramBotWrapper(TOKEN)


@bot.message_handler(commands=["start"])
def start_message(message):
    uid = message.chat.id
    category(uid)
