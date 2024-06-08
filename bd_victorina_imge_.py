import sqlite3, os


# def convert_to_binary_data(filename):
#     # Преобразование данных в двоичный формат
#     with open(filename, "rb") as file:
#         blob_data = file.read()
#     return blob_data


# def insert_blob(photo):
#     try:
#         sqlite_connection = sqlite3.connect("victorina_max.db")
#         cursor = sqlite_connection.cursor()

#         cursor.execute(
#             """
#             CREATE TABLE IF NOT EXISTS pict (
#                 id INTEGER PRIMARY KEY,
#                 imge BLOB
#             );
#             """
#         )

#         sqlite_insert_blob_query = """INSERT INTO pict (imge) VALUES (?)"""

#         emp_photo = convert_to_binary_data(photo)
#         data_tuple = (emp_photo,)
#         cursor.execute(sqlite_insert_blob_query, data_tuple)
#         sqlite_connection.commit()
#         print("Изображение успешно вставлено как BLOB в таблицу")
#         cursor.close()

#     except sqlite3.Error as error:
#         print("Ошибка при работе с SQLite", error)
#     finally:
#         if sqlite_connection:
#             sqlite_connection.close()
#             print("Соединение с SQLite закрыто")


# x = [
#     "db_data1.jpg",
#     "db_data2.jpg",
#     "db_data3.jpg",
#     "db_data4.jpg",
#     "db_data5.jpg",
#     "db_data6.jpg",
#     "db_data7.jpg",
#     "db_data8.jpg",
# ]
# for img in x:
#     insert_blob(img)

# ========================= ПОЛУЧЕНИЕ =======================================


def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, "wb") as file:
        file.write(data)
    print("Данный из blob сохранены в: ", filename, "\n")


def read_blob_data():
    try:
        sqlite_connection = sqlite3.connect("bd_victorina.db")
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_fetch_blob_query = """SELECT * FROM imeg """
        cursor.execute(sql_fetch_blob_query)

        record = cursor.fetchall()

        for row in record:
            photo = row[1]
            photo_path = os.path.join("db_data" + str(row[0]) + ".jpg")
            write_to_file(photo, photo_path)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


read_blob_data()
