import os
from dotenv import load_dotenv

load_dotenv()


VK_TOKEN = os.getenv(
    "VK_TOKEN"
)


GROUP_ID = int(
    os.getenv("GROUP_ID")
)


CERTIFICATE_PATH = "certificate.jpg"