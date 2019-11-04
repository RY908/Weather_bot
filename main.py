from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
# linebot.modelsから処理したいイベントをimport
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, VideoMessage,
    FollowEvent, UnfollowEvent, PostbackEvent, TemplateSendMessage,
    ButtonsTemplate, CarouselTemplate, CarouselColumn, PostbackTemplateAction
)
from linebot.exceptions import LineBotApiError

import scrape as sc
import urllib3.request
import os
import json
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from spreadsheet import EditSpreadSheet

from upload import uploadVideo

import re

 
app = Flask(__name__)

#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']
 
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
    # handleの処理を終えればOK
    return 'OK'
 
## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id 
    worksheet = EditSpreadSheet()
    if '位置情報' in text:
        worksheet.add_user_id(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            [
            TextSendMessage(text='位置情報を教えてください。'),
            TextSendMessage(text='line://nv/location')
            ]
        )

    elif re.match('20\d{6}.+', text):
        """
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )"""
        path = " https://rn-1.herokuapp.com/static/videos/" + user_id + ".mp4"
        new_path = text + ".mp4"
        if not os.path.exists(path):
            os.rename(path, new_path)  
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )
        uploadVideo(new_path)

    else:
        """
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        path = path + '/info.json'
        with open(path) as f:
            d_update = json.load(f)
            #result = (json.load(f))
        d_update[user_id] = 'a'
        result = d_update[user_id]
        with open (path, 'w') as f:
            json.dump(d_update, f)"""
        result = "test"
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']

        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        path += '/rn-1-a615ac4d9dff.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('info').sheet1

        wks.update_acell('A1', 'testtest')
        #print(wks.acell('A1'))

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )
  
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    worksheet = EditSpreadSheet()
    user_id = event.source.user_id
    text = event.message.address

    result, location = sc.get_weather_from_location(text)
    worksheet.add_user_location(user_id, location)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result)
    )

@handler.add(MessageEvent, message=VideoMessage)
def handle_video(event):
    message_id = event.message.id
    user_id = event.source.user_id 
    message_content = line_bot_api.get_message_content(message_id)
    path = "static/videos/" + user_id + ".mp4"
    with open(path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='ファイル名を送信してください。')
    )
    uploadVideo(path)


# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)