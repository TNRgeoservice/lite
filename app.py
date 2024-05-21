from flask import Flask, request, abort
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("ooo6bXW1SokScQJ62nyCadW3j1vdmlLlCE1C7bodbsXDSCg1ojkRiz+8CV6oTMhniE+EdbB1aYSrTnq6M3t7PEgn26Nd6fTpLHbFYlFmrRaGc0wEdBi8HOVwgFQZ3+XnmbWTQiXZWxbkz/wpJveJPQdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.getenv("e4b63a1dd4c9cd09bd74fc2309f66262")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
