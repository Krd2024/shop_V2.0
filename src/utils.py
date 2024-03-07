import sqlite3
import telebot
from telebot import types
from src.wrapper_bot import TelegramBotWrapper

from decouple import config

TOKEN = config("TOKEN", cast=str, default="пусто")

bot = TelegramBotWrapper(TOKEN)


def category(uid, update=None, call=None):
    """Выаодит список категорий в при запуске , if update is None: обновляет экран"""

    with sqlite3.connect("shop_2.db") as connection:
        cursor = connection.cursor()
        cursor.execute(""" SELECT * FROM Category """)
        res = cursor.fetchall()

    key1 = types.InlineKeyboardButton(f"{res[0][1]}", callback_data=f"kateg{res[0][0]}")
    key2 = types.InlineKeyboardButton(f"{res[1][1]}", callback_data=f"kateg{res[1][0]}")
    key3 = types.InlineKeyboardButton(f"{res[2][1]}", callback_data=f"kateg{res[2][0]}")
    key4 = types.InlineKeyboardButton(f"{res[3][1]}", callback_data=f"kateg{res[3][0]}")
    key_basket = types.InlineKeyboardButton("Корзина", callback_data=f"basket")

    add = [key1, key2]
    add1 = [key3, key4]
    keyboard = types.InlineKeyboardMarkup([add, add1, [key_basket]])
    if update is None:
        bot.send_message(uid, text="Выберите категорию товаров:", reply_markup=keyboard)
    else:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Выберите категорию товаров: ⬇️⬇️⬇️",
            reply_markup=keyboard,
        )


def tovar(cat_num):
    """принимает номер категории и выводит из таблицы товары этой категории"""

    with sqlite3.connect("shop_2.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """ SELECT id,name FROM Product WHERE category_id =?""", (cat_num,)
        )
        res_tovar = cursor.fetchall()
        return res_tovar


def specific_product(id_tovar):
    with sqlite3.connect("shop_2.db") as connection:
        cursor = connection.cursor()
        cursor.execute(""" SELECT * FROM Product WHERE id =?""", (id_tovar,))
        res_info = cursor.fetchall()
        return res_info


def basket(uid, prod_id=None):
    with sqlite3.connect("shop_2.db") as connection:
        cursor = connection.cursor()
        if prod_id is not None:
            cursor.execute(
                """ SELECT * FROM Basket WHERE user_id =? AND product_id=?""",
                (
                    uid,
                    prod_id,
                ),
            )
            info_basket = cursor.fetchall()
            return info_basket
        else:
            cursor.execute(
                """ SELECT Product.name,qty,price
                    FROM Basket
                    join Product on Basket.product_id=Product.id
                    WHERE Basket.user_id=?
                """,
                (uid,),
            )
            info_basket = cursor.fetchall()
            return info_basket


def product(res, call):

    chat_id = call.message.chat.id
    message_id = call.message.message_id
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(res)):
        key = types.InlineKeyboardButton(
            f"{res[i][1]}", callback_data=f"prod_id{res[i][0]}"  # callback = id product
        )
        keyboard.add(key)
    key_back_1 = types.InlineKeyboardButton("⬅️ Назад", callback_data=f"back_category")
    keyboard.add(key_back_1)

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Выберите товар: ⬇️⬇️⬇️⬇️⬇️⬇️⬇️",
        reply_markup=keyboard,
    )


# def add_basket(uid, prod_id, action):
#     print(uid, prod_id, action, "<<< test 2")

#     with sqlite3.connect("shop_2.db") as connection:
#         cursor = connection.cursor()
#         if action == "pls":
#             cursor.execute(
#                 """
#                     INSERT INTO  Basket (product_id, qty, user_id )
#                     VALUES (?, ?, ?)

#                     ON CONFLICT(product_id) DO UPDATE SET
#                         qty = CASE
#                                     WHEN qty = 0 THEN 1
#                                     ELSE qty + 1

#                                 END
#                     WHERE user_id = ?;
#                     """,
#                 (
#                     prod_id,
#                     1,
#                     uid,
#                     uid,
#                 ),
#             )
#         elif action == "min":
#             cursor.execute(
#                 """
#                     INSERT INTO  Basket (product_id, qty, user_id )
#                     VALUES (?, ?, ?)
#                     ON CONFLICT(product_id) DO UPDATE SET
#                         qty = CASE
#                                     WHEN qty = 0 THEN 0
#                                     ELSE qty - 1
#                                 END;
#                     """,
#                 (
#                     prod_id,
#                     1,
#                     uid,
#                 ),
#             )

#     connection.commit()


def choice_product(call, prod_id, res_info=None):
    uid = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    res_info = specific_product(prod_id)
    print(prod_id, "<<< ==== test")

    info_basket = basket(uid, prod_id)

    print(info_basket, "<<< -------- КОРЗИНА")

    if info_basket == []:
        kol_vo = 0
    else:
        kol_vo = int(info_basket[0][1])

    key1 = types.InlineKeyboardButton(f"➕", callback_data=f"pls{res_info[0][0]}")
    key2 = types.InlineKeyboardButton(f"➖", callback_data=f"min{res_info[0][0]}")

    key3 = types.InlineKeyboardButton(
        f"Выбрано {kol_vo}({res_info[0][4] * kol_vo}р) ", callback_data=f" "
    )
    key_back_2 = types.InlineKeyboardButton(
        "⬅️ Назад", callback_data=f"bac_k{res_info[0][5]}"
    )

    add = [key2, key1]
    add1 = [key3]
    keyboard = types.InlineKeyboardMarkup([add, add1, [key_back_2]])
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"{res_info[0][1]}⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️\nЦена: {res_info[0][4]} ",
            reply_markup=keyboard,
        )
    except Exception as e:
        print(e)
    finally:
        ...


def screen_basket(call):
    uid = call.from_user.id
    res_basket = basket(uid)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton("Купить", callback_data="yes")
    key1 = types.InlineKeyboardButton(
        "⬅️⬅️⬅️ Продолжить покупки ⬅️⬅️⬅️ ", callback_data="ba_ck"
    )
    keyboard.add(key)
    keyboard.add(key1)
    text = "Товары в корзине:"
    total = 0
    for i in range(len(res_basket)):
        total += res_basket[i][1] * res_basket[i][2]
        text += f"\n{res_basket[i][0]} {res_basket[i][1]}x{res_basket[i][2]}={res_basket[i][1]*res_basket[i][2]}"
    text += f"\n--------\nИтого: {total}"
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboard,
    )


def add2_basket(uid, prod_id, action):

    with sqlite3.connect("shop_2.db") as connection:
        cursor = connection.cursor()

        cursor.execute(
            """ SELECT * FROM Basket WHERE user_id =? AND product_id=?""",
            (
                uid,
                prod_id,
            ),
        )
        info_basket = cursor.fetchall()

        # print(info_basket)
        if info_basket == []:
            if action == "pls":
                cursor.execute(
                    """INSERT INTO Basket (product_id,qty,user_id) VALUES (?,?,?)""",
                    (
                        prod_id,
                        1,
                        uid,
                    ),
                )
            elif action == "min":
                print("Нечего отнимать")
        else:
            qty = info_basket[0][1]
            qty += 1
            cursor.execute(
                """UPDATE Basket SET product_id=?,qty=?,user_id=? WHERE user_id=?""",
                (
                    prod_id,
                    qty,
                    uid,
                    uid,
                ),
            )
            print(prod_id, qty, uid)
        connection.commit()
        with sqlite3.connect("shop_2.db") as connection:
            cursor = connection.cursor()

        cursor.execute(
            """ SELECT * FROM Basket WHERE user_id =? AND product_id=?""",
            (
                uid,
                prod_id,
            ),
        )
        info_basket = cursor.fetchall()

        print(info_basket, "<<< ===== test")
