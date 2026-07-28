import sqlite3

from datetime import datetime

DB_NAME = "users.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            vk_id INTEGER UNIQUE,

            ref TEXT,

            first_visit TEXT,

            subscribed INTEGER DEFAULT 0,

            certificate_sent INTEGER DEFAULT 0

        )
    """)    

    conn.commit()
    conn.close()

def add_user(vk_id, ref=None):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO users
        (
            vk_id,
            ref,
            first_visit
        )

        VALUES (?, ?, datetime('now'))


        ON CONFLICT(vk_id)

        DO UPDATE SET

            ref = COALESCE(users.ref, excluded.ref)

    """,
    (
        vk_id,
        ref
    ))


    conn.commit()

    conn.close()

def update_subscription(vk_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET subscribed = 1
        WHERE vk_id = ?
    """, (vk_id,))


    conn.commit()
    conn.close()

def update_certificate(vk_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET certificate_sent = 1
        WHERE vk_id = ?
    """, (vk_id,))


    conn.commit()
    conn.close()

def certificate_already_sent(vk_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""
        SELECT certificate_sent
        FROM users
        WHERE vk_id = ?
    """,
    (vk_id,))


    result = cursor.fetchone()


    conn.close()


    if result:

        return result[0] == 1


    return False

def get_statistics():


    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    # Всего пользователей

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    total = cursor.fetchone()[0]


    # Подписки

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE subscribed = 1
        """
    )

    subscribed = cursor.fetchone()[0]


    # Сертификаты

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE certificate_sent = 1
        """
    )

    certificates = cursor.fetchone()[0]


    # Источники

    cursor.execute(
        """
        SELECT ref, COUNT(*)
        FROM users
        GROUP BY ref
        """
    )


    refs = cursor.fetchall()


    conn.close()


    return total, subscribed, certificates, refs