import vk_api

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from config import (
    VK_TOKEN,
    GROUP_ID,
    CERTIFICATE_PATH,
    ADMIN_ID
)

from database import (
    create_database,
    add_user,
    add_source,
    add_event,
    event_exists,
    update_subscription,
    update_certificate,
    certificate_already_sent,
    get_statistics
)


# ======================================
# Подключение VK API
# ======================================

vk_session = vk_api.VkApi(
    token=VK_TOKEN
)

vk = vk_session.get_api()


# ======================================
# Создание базы данных
# ======================================

create_database()



# ======================================
# Проверка подписки
# ======================================

def check_subscription(user_id):

    result = vk.groups.isMember(
        group_id=GROUP_ID,
        user_id=user_id
    )

    return result == 1



# ======================================
# Клавиатура
# ======================================

def create_keyboard():

    keyboard = VkKeyboard(
        inline=True
    )


    keyboard.add_openlink_button(
        "Подписаться на сообщество",
        "https://vk.ru/club240524894"
    )


    keyboard.add_line()


    keyboard.add_button(
        "Проверить подписку",
        color=VkKeyboardColor.PRIMARY
    )


    return keyboard.get_keyboard()



# ======================================
# Отправка сообщения
# ======================================

def send_message(
        user_id,
        text,
        keyboard=None
):

    vk.messages.send(

        user_id=user_id,

        random_id=0,

        message=text,

        keyboard=keyboard
    )



# ======================================
# Отправка фотографии сертификата
# ======================================

def send_photo(user_id):

    upload = vk_api.VkUpload(
        vk_session
    )


    photo = upload.photo_messages(
        CERTIFICATE_PATH
    )


    attachment = (
        f"photo{photo[0]['owner_id']}_"
        f"{photo[0]['id']}"
    )


    vk.messages.send(

        user_id=user_id,

        random_id=0,

        attachment=attachment
    )



# ======================================
# Отправка сертификата
# ======================================

def send_certificate(user_id):


    # Проверяем, был ли сертификат раньше

    if certificate_already_sent(user_id):

        send_message(

            user_id,

            """
🎁 Вы уже получали сертификат.

Спасибо за участие!
"""
        )

        return



    send_message(

        user_id,

        """
🎁 Ваш сертификат готов!


Условия использования:

- действует 30 дней
- один сертификат на пользователя
- предъявите его при покупке
"""
    )


    send_photo(
        user_id
    )


    update_certificate(
        user_id
    )


    if not event_exists(
        user_id,
        "certificate"
    ):

        add_event(
            user_id,
            "certificate"
        )



# ======================================
# Формирование статистики
# ======================================

def create_statistics_message():


    total, subscribed, certificates, refs = get_statistics()


    message = f"""
📊 Статистика лидогенерации


👥 Всего пользователей:
{total}


✅ Подписались:
{subscribed}


🎁 Получили сертификат:
{certificates}


📌 Источники переходов:
"""


    if refs:

        for ref, count in refs:

            message += (
                f"\n{ref} — {count}"
            )

    else:

        message += "\nНет данных"



    return message



# ======================================
# Обработка сообщений
# ======================================

def process_message(message):


    user_id = message["from_id"]


    text = message.get(
        "text",
        ""
    ).lower()



    # -------------------------------
    # Статистика администратора
    # -------------------------------

    if text == "статистика":


        if user_id == ADMIN_ID:


            send_message(

                user_id,

                create_statistics_message()

            )


        else:


            send_message(

                user_id,

                "⛔ Нет доступа."

            )


        return



    # -------------------------------
    # Источник перехода
    # -------------------------------

    ref = message.get(
        "ref"
    ) or "unknown"



    # -------------------------------
    # Добавление пользователя
    # -------------------------------

    new_user = add_user(

        user_id,

        ref

    )


    if new_user:


        add_source(
            ref
        )


        add_event(

            user_id,

            "start"

        )



    # -------------------------------
    # Команда Начать
    # -------------------------------

    if text == "начать":



        if check_subscription(
            user_id
        ):


            update_subscription(
                user_id
            )


            if not event_exists(

                user_id,

                "subscribe"

            ):

                add_event(

                    user_id,

                    "subscribe"

                )


            send_certificate(

                user_id

            )



        else:


            send_message(

                user_id,


                """
Для получения сертификата необходимо подписаться на наше сообщество.

После подписки нажмите кнопку "Проверить подписку".
""",


                create_keyboard()

            )



    # -------------------------------
    # Проверка подписки
    # -------------------------------

    elif text == "проверить подписку":



        if check_subscription(
            user_id
        ):



            update_subscription(

                user_id

            )


            if not event_exists(

                user_id,

                "subscribe"

            ):


                add_event(

                    user_id,

                    "subscribe"

                )


            send_certificate(

                user_id

            )



        else:


            send_message(

                user_id,


                """
Подписка не найдена.

Пожалуйста, подпишитесь на наше сообщество.
""",


                create_keyboard()

            )