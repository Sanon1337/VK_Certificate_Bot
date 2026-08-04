import time
import vk_api

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from config import (
    VK_TOKEN,
    REMINDER_IMAGE_PATH
)

from database import (
    get_users_for_reminder,
    update_reminder
)


# ======================================
# Подключение VK API
# ======================================

vk_session = vk_api.VkApi(
    token=VK_TOKEN
)

vk = vk_session.get_api()

upload = vk_api.VkUpload(
    vk_session
)



# ======================================
# Клавиатура
# ======================================

def create_keyboard():

    keyboard = VkKeyboard(
        inline=True
    )


    keyboard.add_openlink_button(
        "➡️ Подписаться",
        "https://vk.ru/club240524894"
    )


    keyboard.add_line()


    keyboard.add_button(
        "✅ Проверить подписку",
        color=VkKeyboardColor.PRIMARY
    )


    return keyboard.get_keyboard()



# ======================================
# Отправка напоминания
# ======================================

def send_reminder(user_id):


    photo = upload.photo_messages(
        REMINDER_IMAGE_PATH
    )


    attachment = (
        f"photo{photo[0]['owner_id']}_"
        f"{photo[0]['id']}"
    )


    vk.messages.send(

        user_id=user_id,

        random_id=0,

        attachment=attachment,

        message="""
🎁 Остался всего один шаг...

Ваш сертификат всё ещё ждёт вас - проверьте подписку и заберите подарок!
""",

        keyboard=create_keyboard()

    )



# ======================================
# Запуск проверки
# ======================================

while True:


    users = get_users_for_reminder()


    for user_id in users:

        try:

            send_reminder(
                user_id
            )


            update_reminder(
                user_id
            )


            print(
                f"Напоминание отправлено: {user_id}"
            )


        except Exception as e:


            print(
                f"Ошибка отправки {user_id}: {e}"
            )



    # проверяем каждый час

    time.sleep(
        3600
    )