from telebot import types
from src.wrapper_bot import TelegramBotWrapper
from src.utils import *

from decouple import config

TOKEN = config("TOKEN", cast=str, default="пусто")
bot = TelegramBotWrapper(TOKEN)


@bot.callback_query_handler(func=lambda call: call.data.startswith(("kateg", "back")))
def handle_answer1(call):
    uid = call.from_user.id
    if call.data.startswith("back"):
        uid = call.from_user.id
        update = 1
        category(uid, update, call)
        return

    print(call.data, " <<<<=========== callback из меню")
    category_number = call.data[5:]
    res = tovar(category_number)
    print(res, " <<<<=========== Категория")

    product(res, call)


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(("bac_k", "prod_id"))
)
def handle_answer2(call):
    """получение,вывод,добавление в корзину конкретного товара"""

    if call.data.startswith("prod_id"):
        res_info = specific_product(call.data[7:])
        print(res_info, "<<< ----- карточка товара")
        choice_product(call, call.data[7:], res_info)

    elif call.data.startswith("bac_k"):
        print(call.data, "<<< ----- call bac_k")
        res = tovar(call.data[5:])

        product(res, call)
        return


@bot.callback_query_handler(func=lambda call: call.data.startswith(("pls", "min")))
def handle_(call):
    uid = call.from_user.id
    prod_id = call.data[3:]
    action = call.data[:3]
    add_basket(uid, prod_id, action)
    # print(call)
    choice_product(call, prod_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("basket"))
def handle_(call):
    uid = call.from_user.id
    res_basket = basket(uid)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton("Купить", callback_data="yes")
    keyboard.add(key)
    text = "Товары в корзине:"
    total = 0
    for i in range(len(res_basket)):
        total += res_basket[i][1] * res_basket[i][2]
        text += f"\n{res_basket[i][0]} {res_basket[i][1]}✖️{res_basket[i][2]}🟰{res_basket[i][1]*res_basket[i][2]}"
    text += f"\n--------\nИтого: {total}"
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboard,
    )


bot.infinity_polling()
