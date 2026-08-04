import sqlite3

DB_NAME = "users.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    # Таблица пользователей

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            vk_id INTEGER UNIQUE,

            ref TEXT,

            first_visit TEXT,

            subscribed INTEGER DEFAULT 0,

            certificate_sent INTEGER DEFAULT 0,

            reminder_sent INTEGER DEFAULT 0

        )
    """)



    # Таблица источников

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ref TEXT UNIQUE,

            users_count INTEGER DEFAULT 0

        )
    """)

    # Таблица событий пользователей

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            vk_id INTEGER,

            event_name TEXT,

            event_date TEXT,

            UNIQUE(vk_id,event_name)

        )
    """)

    conn.commit()

    conn.close()

def add_user(vk_id, ref=None):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute(
        "SELECT id FROM users WHERE vk_id=?",
        (vk_id,)
    )


    user = cursor.fetchone()



    if user:

        conn.close()

        return False



    cursor.execute("""
        INSERT INTO users
        (
            vk_id,
            ref,
            first_visit
        )

        VALUES
        (
            ?,
            ?,
            datetime('now')
        )

    """,
    (
        vk_id,
        ref
    ))


    conn.commit()

    conn.close()


    return True

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
    SELECT ref, users_count
    FROM sources
    """
)

    refs = cursor.fetchall()


    conn.close()


    return total, subscribed, certificates, refs

def add_source(ref):

    if not ref:
        ref = "unknown"


    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO sources
        (
            ref,
            users_count
        )

        VALUES
        (
            ?,
            1
        )


        ON CONFLICT(ref)

        DO UPDATE SET

            users_count = users_count + 1

    """,
    (
        ref,
    ))


    conn.commit()

    conn.close()

def add_event(vk_id, event):

    if event_exists(vk_id, event):
        return False


    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO events
        (
            vk_id,
            event_name,
            event_date
        )

        VALUES
        (
            ?,
            ?,
            datetime('now')
        )

    """,
    (
        vk_id,
        event
    ))


    conn.commit()

    conn.close()


    return True

def event_exists(vk_id, event):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""
        SELECT id
        FROM events
        WHERE vk_id = ?
        AND event_name = ?
    """,
    (
        vk_id,
        event
    ))


    result = cursor.fetchone()


    conn.close()


    return result is not None
<<<<<<< HEAD

def get_users_for_reminder():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""
        SELECT vk_id
        FROM users
        WHERE certificate_sent = 0
        AND reminder_sent = 0
        AND datetime(first_visit) <= datetime('now', '-3 hours')
    """)


    users = cursor.fetchall()


    conn.close()


    return [
        user[0]
        for user in users
    ]



def update_reminder(vk_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""
        UPDATE users
        SET reminder_sent = 1
        WHERE vk_id = ?
    """,
    (
        vk_id,
    ))


    conn.commit()

    conn.close()
=======
>>>>>>> ffdaf9727c0236415ca2961709e7c04d4ec55b9f
