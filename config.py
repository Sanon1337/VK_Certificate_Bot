import os

from dotenv import load_dotenv


load_dotenv()



# =====================================
# Получение переменных окружения
# =====================================

VK_TOKEN = os.getenv(
    "VK_TOKEN"
)


GROUP_ID = os.getenv(
    "GROUP_ID"
)


ADMIN_ID = os.getenv(
    "ADMIN_ID"
)



# =====================================
# Проверка настроек
# =====================================

if not VK_TOKEN:

    raise ValueError(
        "Не найден VK_TOKEN в .env"
    )


if not GROUP_ID:

    raise ValueError(
        "Не найден GROUP_ID в .env"
    )


if not ADMIN_ID:

    raise ValueError(
        "Не найден ADMIN_ID в .env"
    )



# =====================================
# Преобразование типов
# =====================================

GROUP_ID = int(
    GROUP_ID
)


ADMIN_ID = int(
    ADMIN_ID
)



# =====================================
# Файл сертификата
# =====================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


CERTIFICATE_PATH = os.path.join(
    BASE_DIR,
    "certificate.jpg"
)