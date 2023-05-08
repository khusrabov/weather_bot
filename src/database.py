# in dev
import sqlite3


# Now only the creation of a database is implemented, to which users who have written are added /subscribe 'city'
def create_table():
    conn = sqlite3.connect('subscriptions.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS subscriptions'
              '(chat_id int, city_name text, time text)')

    conn.commit()
    conn.close()


def add_subscription(chat_id, city_name, time):
    # Открываем соединение с базой данных
    conn = sqlite3.connect('subscriptions.db')

    # Добавляем новую подписку в таблицу subscriptions
    conn.execute("INSERT INTO subscriptions (chat_id, city_name, time) \
                  VALUES (?, ?, ?)", (chat_id, city_name, time))

    # Сохраняем изменения в базе данных
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()
