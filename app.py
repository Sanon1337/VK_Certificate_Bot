from flask import Flask, request

from bot import process_message

from config import CONFIRMATION_CODE

app = Flask(__name__)




@app.route("/", methods=["POST"])
def callback():


    data = request.get_json()

    print(data, flush=True)



    if not data:

        return "empty"



    # =================================
    # Подтверждение Callback API VK
    # =================================

    if data["type"] == "confirmation":

        return CONFIRMATION_CODE



    # =================================
    # Новое сообщение пользователю
    # =================================

    elif data["type"] == "message_new":


        try:

            message = data["object"]["message"]


            process_message(
                message
            )


        except Exception as error:

            print(
                "Ошибка обработки сообщения:",
                error,
		flush=True
            )



    # =================================
    # Остальные события игнорируем
    # =================================

    else:

        print(
            "Неизвестное событие:",
            data["type"]
        )



    return "ok"




if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000

    )
