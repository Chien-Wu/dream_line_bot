import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, abort
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, ReplyMessageRequest, TextMessage
from linebot.v3.webhook import WebhookHandler, MessageEvent
from linebot.v3.exceptions import InvalidSignatureError
import openai
import redis
import json

from message_handler import generate_reply

app = Flask(__name__)

config = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
messaging_api = MessagingApi(ApiClient(config))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai.api_key = os.getenv("OPENAI_API_KEY")

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(redis_url, decode_responses=True)

def load_user_history(user_id):
    data = r.get(f"user_history:{user_id}")
    if data:
        return json.loads(data)
    return []

def save_user_history(user_id, history, ttl=86400):
    r.set(f"user_history:{user_id}", json.dumps(history), ex=ttl)

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
        user_id = event.source.user_id
        user_text = event.message.text

        # 用 Redis 拿歷史
        history = load_user_history(user_id)

        gpt_reply = generate_reply(user_id, user_text, user_history=history)

        # 寫回歷史（最多只留 10 輪）
        history = history + [
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": gpt_reply},
        ]
        save_user_history(user_id, history[-10:])

        reply = ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=gpt_reply)]
        )
        messaging_api.reply_message(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
