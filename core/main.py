import requests
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
port = int(os.environ.get('PORT', 3002))


def send_notification(message=None):
    s = requests.post(os.environ.get("WEB_HOOK_URL"), json={
        "cards": [
            {
                "header": {
                    "title": os.environ.get("BOT_NAME"),
                    "subtitle": os.environ.get("PROJECT_NAME")
                },
                "sections": [
                    {
                        "header": message['code'] if message else "Server Monitor Running",
                        "widgets": [
                            {
                                "textParagraph": {
                                    "text": message['body'] if message else "All PM2 errors will be sent here"
                                }
                            }
                        ]
                    }
                ]
            }
        ]

    })

    if s.status_code == 200:
        print("Error Reported Successfully")
    else:
        print(
            f'Failed to send Report. Status code: {s.status_code}')


# try:
#     print("Starting Server")
#     send_notification()
# except Exception:
#     print(Exception)


@app.route("/", methods=["POST"])
def root():
    try:
        print(request.json)
        send_notification(request.json)
        return jsonify({"status": "success", "message": "This error has been reported"}), 200
    except Exception:
        print(Exception)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=port)
