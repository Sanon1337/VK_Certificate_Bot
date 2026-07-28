from flask import Flask, request

from bot import process_message


app = Flask(__name__)


CONFIRMATION_CODE = "4519411f"


@app.route("/", methods=["POST"])
def callback():

    data = request.json

    print(data)


    # Подтверждение сервера VK

    if data["type"] == "confirmation":

        return CONFIRMATION_CODE



    # Новое сообщение от пользователя

    if data["type"] == "message_new":

        message = data["object"]["message"]

        process_message(
            message
        )


    return "ok"



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )