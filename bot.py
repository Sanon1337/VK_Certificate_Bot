import vk_api

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from config import (
    VK_TOKEN,
    GROUP_ID,
    CERTIFICATE_PATH
)

from database import (
    create_database,
    add_user,
    update_subscription,
    update_certificate,
    certificate_already_sent,
    get_statistics
)


# Подключение VK API

vk_session = vk_api.VkApi(
    token=VK_TOKEN
)

vk = vk_session.get_api()


# Создание БД

create_database()



# -------------------------------
# Проверка подписки
# -------------------------------

def check_subscription(user_id):

    result = vk.groups.isMember(
        group_id=GROUP_ID,
        user_id=user_id
    )

    return result == 1



# -------------------------------
# Клавиатура
# -------------------------------

def create_keyboard():

    keyboard = VkKeyboard(
        inline=True
    )


    keyboard.add_button(
        "Проверить подписку",
        color=VkKeyboardColor.PRIMARY
    )


    return keyboard.get_keyboard()



# -------------------------------
# Отправка сообщения
# -------------------------------

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



# -------------------------------
# Отправка сертификата
# -------------------------------

def send_certificate(user_id):


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


    upload = vk_api.VkUpload(
        vk_session
    )


    photo = upload.photo_messages(
        CERTIFICATE_PATH
    )


    vk.messages.send(

        user_id=user_id,

        random_id=0,

        attachment=
        f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
    )


    update_certificate(user_id)



# -------------------------------
# Главная обработка сообщений
# -------------------------------

def process_message(message):


    user_id = message["from_id"]

    text = message["text"].lower()


    # Получаем источник перехода

    ref = message.get("ref")


    # Добавляем пользователя

    add_user(
        user_id,
        ref
    )



    # =========================
    # Команда "Начать"
    # =========================

    if text == "начать":


        # Проверяем подписку

        if check_subscription(user_id):


            update_subscription(
                user_id
            )


            # Проверяем, выдавался ли сертификат

            if certificate_already_sent(user_id):


                send_message(

                    user_id,

                    """
Вы уже получили свой сертификат 🎁

Спасибо за участие!
"""
                )


            else:


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



    # =========================
    # Проверка подписки
    # =========================

    elif text == "проверить подписку":


        if check_subscription(user_id):


            update_subscription(
                user_id
            )



            if certificate_already_sent(user_id):


                send_message(

                    user_id,

                    """
Вы уже получали сертификат 🎁
"""
                )


            else:


                send_certificate(
                    user_id
                )



        else:


            send_message(

                user_id,


                """
Подписка не найдена.

Пожалуйста, подпишитесь на наше сообщество.
"""
            )



    # =========================
    # Статистика
    # =========================

    elif text == "статистика":


        total, subscribed, certificates, refs = get_statistics()


        stats = f"""
📊 Статистика бота


Всего пользователей:
{total}


Подписались:
{subscribed}


Получили сертификат:
{certificates}


Источники:
"""


        for ref_name, count in refs:

            stats += f"\n{ref_name}: {count}"



        send_message(

            user_id,

            stats

        )