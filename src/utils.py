import datetime
import sqlite3
import telebot
from telebot import types
from telegram import InputMediaPhoto, Update
from src.wrapper_bot import TelegramBotWrapper
import time

from decouple import config

TOKEN = config("TOKEN", cast=str, default="пусто")

bot = TelegramBotWrapper(TOKEN)


def category(uid, update=None, call=None):
    """Выводит список категорий в при запуске , if update is None: обновляет экран"""

    with sqlite3.connect("shop_2.db") as connection:
        cursor = connection.cursor()
        cursor.execute(""" SELECT * FROM Category """)
        res = cursor.fetchall()

    key1 = types.InlineKeyboardButton(f"{res[0][1]}", callback_data=f"kateg{res[0][0]}")
    key2 = types.InlineKeyboardButton(f"{res[1][1]}", callback_data=f"kateg{res[1][0]}")
    key3 = types.InlineKeyboardButton(f"{res[2][1]}", callback_data=f"kateg{res[2][0]}")
    key4 = types.InlineKeyboardButton(f"{res[3][1]}", callback_data=f"kateg{res[3][0]}")
    get_orders = types.InlineKeyboardButton(
        f"Посмотреть покупки", callback_data=f"get_orders"
    )
    key_basket = types.InlineKeyboardButton("Корзина", callback_data=f"basket")

    add = [key1, key2]
    add1 = [key3, key4]
    keyboard = types.InlineKeyboardMarkup([add, add1, [get_orders], [key_basket]])
    if update is None:
        bot.send_message(uid, text="Выберите категорию товаров:", reply_markup=keyboard)
    else:
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Выберите категорию товаров:\n⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️",
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
    """Возвращает инф.товара по id"""

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
        text="Выберите товар:\n⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️",
        reply_markup=keyboard,
    )


def get_img(id_img):
    with sqlite3.connect("shop_2.db") as connection:
        cursor = connection.cursor()

        cursor.execute(
            """ SELECT file_path FROM Img WHERE id =?""",
            (id_img,),
        )
        info_basket = cursor.fetchone()[0]
        return info_basket


def choice_product(call, prod_id, res_info=None):
    uid = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    # ----------------------------------------------------------------
    res_info = specific_product(prod_id)  # Выбор конретного товара
    balance = res_info[0][3]  # остаток товара
    # ---------------------- картинка---------------------------------
    {res_info[0][1]}  # наиминование продукта
    prod_id  # id продукта
    img_id = res_info[0][2]  # id img
    path_img = get_img(img_id)

    file_img = open(path_img, "rb")

    # ----------------------------------------------------------------
    print(prod_id, "<<< ==== test")
    info_basket = basket(uid, prod_id)
    print(info_basket, "<<< -------- КОРЗИНА")

    text = (
        f"{res_info[0][1]}\nЦена: {res_info[0][4]}\nОстаток: {balance}\n⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️",
    )
    # bot.edit_message_media(uid, file_img)
    # print(call.inline_message_id)
    # bot.edit_message_media(
    #     media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None
    # )

    # bot.send_photo(uid, file_img, caption=text)

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
    # ----------------------------------------------------------------
    with open(path_img, "rb") as photo_file:
        photo_media = photo_file.read()
    # --------------------------------------------------------------
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"{res_info[0][1]}\nЦена: {res_info[0][4]}\nОстаток: {balance}\n⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️",
            reply_markup=keyboard,
        )
    except Exception as e:
        print(e)
    finally:
        ...


def screen_basket(call, end=None):
    """Показать содержимое корзины при запросе"""

    uid = call.from_user.id
    res_basket = basket(uid)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    keyboard = types.InlineKeyboardMarkup()
    if end is not None and end == "Куплено ✔️":
        text = end
    else:
        text = f"Купить"
    if end is not None and end == "Корзина пустая":
        text2 = end
    else:
        text2 = f"Товары в корзине:"
    key = types.InlineKeyboardButton(text, callback_data="yes")
    key1 = types.InlineKeyboardButton("⬅️⬅️⬅️⬅️Главное меню⬅️⬅️⬅️⬅️", callback_data="ba_ck")
    keyboard.add(key)
    keyboard.add(key1)

    total = 0
    for i in range(len(res_basket)):
        total += res_basket[i][1] * res_basket[i][2]
        text2 += f"\n{res_basket[i][0]} {res_basket[i][1]}x{res_basket[i][2]}={res_basket[i][1]*res_basket[i][2]}"
    text2 += f"\n--------\nИтого: {total}"
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text2,
        reply_markup=keyboard,
    )


def add2_basket(uid, prod_id, action):
    """Добавление товара в корзину"""

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
            if action == "pls":
                qty += 1
            else:
                qty -= 1
            cursor.execute(
                """UPDATE Basket SET product_id=?,qty=?,user_id=? WHERE user_id=? AND product_id=? """,
                (
                    prod_id,
                    qty,
                    uid,
                    uid,
                    prod_id,
                ),
            )
        connection.commit()


def order_and_ordeItem(uid, call):
    """Занесение заказа в таблицу"""

    data_time = datetime.datetime.now()
    date = data_time.strftime("%m.%d.%Y")
    time = data_time.strftime("%H:%M")

    with sqlite3.connect("shop_2.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """ SELECT * FROM Basket WHERE user_id =?""",
            (uid,),
        )
        info_basket = cursor.fetchall()
        print(info_basket)
        if info_basket != []:
            cursor.execute(
                """INSERT INTO Orders (user_id,date,time) VALUES (?,?,?)""",
                (uid, date, time),
            )
            connection.commit()
            cursor.execute(
                """ SELECT id FROM Orders WHERE user_id =?""",
                (uid,),
            )
        else:
            end = f"Корзина пустая"
            screen_basket(call, end)
            return
    info_order = cursor.fetchall()[-1][0]  # получить id order

    for i in range(len(info_basket)):
        cursor.execute(
            """INSERT INTO Order_item (order_id,produkt_id,count) VALUES (?,?,?)""",
            (info_order, info_basket[i][0], info_basket[i][1]),
        )

        res_info = specific_product(info_basket[i][0])
        qty = res_info[0][3] - info_basket[i][1]  # вычитание купленного из остатка
        print(qty, uid, info_basket)
        cursor.execute(
            """UPDATE Product SET balance=? WHERE id=? """,
            (
                qty,
                info_basket[i][0],
            ),
        )
    connection.commit()
    # =================================================================
    connection.commit()
    cursor.execute(""" DELETE FROM Basket WHERE user_id =?""", (uid,))
    connection.commit()
    end = f"Куплено ✔️"
    # =================================================================
    # Выбор конретного товара
    # остаток товара

    screen_basket(call, end)  # вывод на экран пустой корзины


def get_orders(uid, call):
    """Показывае совершённые покупки"""

    uid = call.from_user.id
    # res_basket = basket(uid)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    with sqlite3.connect("shop_2.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """SELECT  DISTINCT Product.name,count,Orders.user_id,date,time FROM Order_item
                JOIN Product on Order_item.produkt_id = Product.id
                JOIN Orders on Order_item.order_id = Orders.id
                WHERE Orders.user_id = ?""",
            (uid,),
        )
        res_get_orders = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(f"Вернуться в главное меню", callback_data="main")
    keyboard.add(key)
    text3 = f"Ваши покупки:\n⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️"
    for i in range(len(res_get_orders)):
        text3 += f"\n{res_get_orders[i][0]}\nКоличество: {res_get_orders[i][1]}\nДата: {res_get_orders[i][3]}\nВремя: {res_get_orders[i][4]}\n--------------------------"

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text3,
        reply_markup=keyboard,
    )
    print(res_get_orders)
