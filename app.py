from flask import Flask, request, abort
import os
import openai
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# รับค่า Environment Variables สำหรับ LINE API
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("ooo6bXW1SokScQJ62nyCadW3j1vdmlLlCE1C7bodbsXDSCg1ojkRiz+8CV6oTMhniE+EdbB1aYSrTnq6M3t7PEgn26Nd6fTpLHbFYlFmrRaGc0wEdBi8HOVwgFQZ3+XnmbWTQiXZWxbkz/wpJveJPQdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.getenv("e4b63a1dd4c9cd09bd74fc2309f66262")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# รับค่า Environment Variables สำหรับ OpenAI API
OPENAI_API_KEY = os.getenv("sk-tnr-gpt-TPp1hAYKOL1wZTQtmhqBT3BlbkFJsrHqN93Sr63RLZ4Tayxi")
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
        engine="gpt-4",  # เปลี่ยนเป็น gpt-4
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@handler.add(Messa
