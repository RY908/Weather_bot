from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
# linebot.modelsから処理したいイベントをimport
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage,
    FollowEvent, UnfollowEvent, PostbackEvent, TemplateSendMessage,
    ButtonsTemplate, CarouselTemplate, CarouselColumn, PostbackTemplateAction
)
from linebot.exceptions import LineBotApiError

import scrape as sc
import urllib3.request
import os
import json
import sys

 
app = Flask(__name__)

#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def append_json_to_file(data: dict, path_file: str) -> bool:
    with open(path_file, 'ab+') as f:              # ファイルを開く
        f.seek(0,2)                                # ファイルの末尾（2）に移動（フォフセット0）  
        if f.tell() == 0 :                         # ファイルが空かチェック
            f.write(json.dumps([data]).encode())   # 空の場合は JSON 配列を書き込む
        else :
            f.seek(-1,2)                           # ファイルの末尾（2）から -1 文字移動
            f.truncate()                           # 最後の文字を削除し、JSON 配列を開ける（]の削除）
            f.write(' , '.encode())                # 配列のセパレーターを書き込む
            f.write(json.dumps(data).encode())     # 辞書を JSON 形式でダンプ書き込み
            f.write(']'.encode())                  # JSON 配列を閉じる
    return f.close() # 連続で追加する場合は都度 Open, Close しない方がいいかも

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
  user_id = event.message.id
  if '位置情報' in text:
    line_bot_api.reply_message(
      event.reply_token,
      [
      TextSendMessage(text='位置情報を教えてください。'),
      TextSendMessage(text='line://nv/location')
      ]
    )

  else:
    #result = sc.get_weather(text)
    result = user_id
    data = {
        'id': user_id
    }
    #with open('info.json', 'w') as outfile:
        #json.dump(data, outfile)
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    path = path + '/info.json'
    append_json_to_file(data, path)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result)
    )
  
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    text = event.message.address

    result = sc.get_weather_from_location(text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result)
    )

# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)