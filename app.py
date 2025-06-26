from flask import Flask, request, abort
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, ReplyMessageRequest, TextMessage
from linebot.v3.webhook import WebhookHandler, MessageEvent
from linebot.v3.exceptions import InvalidSignatureError
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

config = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
messaging_api = MessagingApi(ApiClient(config))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent)
def handle_message(event):
    if hasattr(event.message, "text"):
        user_text = event.message.text

        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        gpt_reply = resp.choices[0].message.content
        reply = ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=gpt_reply)]
        )
        messaging_api.reply_message(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
