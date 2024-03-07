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

    # uid = call.from_user.id
    # chat_id = call.message.chat.id
    # message_id = call.message.message_id

    # info_basket = basket(uid, call.data[7:])

    # print(info_basket, "<<< -------- КОРЗИНА")

    # if info_basket == []:
    #     kol_vo = 0
    # else:
    #     kol_vo = int(info_basket[0][1])

    # key1 = types.InlineKeyboardButton(f"➕", callback_data=f"pls{res_info[0][0]}")
    # key2 = types.InlineKeyboardButton(f"➖", callback_data=f"min{res_info[0][0]}")

    # key3 = types.InlineKeyboardButton(
    #     f"Выбрано {kol_vo}({res_info[0][4] * kol_vo}р) ", callback_data=f" "
    # )
    # key_back_2 = types.InlineKeyboardButton(
    #     "⬅️ Назад", callback_data=f"bac_k{res_info[0][5]}"
    # )

    # add = [key2, key1]
    # add1 = [key3]
    # keyboard = types.InlineKeyboardMarkup([add, add1, [key_back_2]])

    # bot.edit_message_text(
    #     chat_id=chat_id,
    #     message_id=message_id,
    #     text=f"{res_info[0][1]}\nЦена: {res_info[0][4]} ",
    #     reply_markup=keyboard,
    # )


@bot.callback_query_handler(func=lambda call: call.data.startswith(("pls", "min")))
def handle_(call):
    uid = call.from_user.id
    prod_id = call.data[3:]
    action = call.data[:3]
    add_basket(uid, prod_id, action)
    # print(call)
    choice_product(call, prod_id)


bot.infinity_polling()
