from flask import Flask, request, abort
import openai
from linebot import WebhookHandler, LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# รับค่า Environment Variables สำหรับ LINE API
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("YOUR_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("YOUR_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("Environment variables for LINE API not set")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# รับค่า Environment Variables สำหรับ OpenAI API
OPENAI_API_KEY = os.getenv("YOUR_OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Environment variable for OpenAI API key not set")
openai.api_key = OPENAI_API_KEY

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def generate_gpt4_response(prompt):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    gpt4_response = generate_gpt4_response(user_message)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=gpt4_response)
    )

if __name__ == "__main__":
    app.run(debug=True)
