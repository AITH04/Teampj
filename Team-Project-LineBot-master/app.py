import os
import requests
import json
import main

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent,
    TextMessage, TextSendMessage
)


app = Flask(__name__)


# 讀取重要TOKEN
with open('linebotToken.json', 'r', encoding='utf8') as f:
    content = json.load(f)
line_bot_api = LineBotApi(content['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(content['YOUR_CHANNEL_SECRET'])
print(":: SYSTEM MSG :: line bot TOKEN 載入成功")


# 呼叫對話引擎API
def callAPIdialog(json_input={"userId": "test000", "msg": "測試資料"}):
    '''
    # 呼叫推薦服務
    :param json_input:
    :return:
    '''
    print('\n::SYS訊息:: 呼叫對話引擎 \n')
    response = requests.post('https://sys0828-a.herokuapp.com/api', json=json_input)
    #response = requests.post('https://7829a192484a.ngrok.io/api', json=json_input)
    response = response.json()
    print('\n::SYS訊息:: retrun content \n', response)
    print('\n::SYS訊息:: return object type: \n', type(response))
    return response


@app.route("/", methods=['GET'])
def hello():
    print(":: SYSTEM MSG :: 有人透過GET呼叫首頁'/'")
    return '看到這個訊息，代表本py檔正常執行'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    user_id = event.source.user_id
    api_par = {"userId": user_id, "msg": msg}
    print(f"api_par: {api_par}")
    # 這邊應該要call API
    pass_par = callAPIdialog(api_par)
    print(f"::賴爸msg:: pss_par=",str(pass_par))
    print(f"data type= {type(pass_par)}")
    reply_msg_element = main.main(pass_par)

    # 測試api_par內容
    #reply_msg_element.append(TextSendMessage(text=f'pai_par內容: {str(api_par)}'))
    #print(f"pass_par: {pass_par}")
    line_bot_api.reply_message( event.reply_token,reply_msg_element)
    print('\n====================================================================================\n\n')


@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name
    print(user_name)
    welcome_word0 = f'{user_name}，您好(hello)！\n感謝您成為送禮達人的好友！\n\n若不想接收提醒，可以點畫面右上方的選單圖示，然後關閉「提醒」喔。\n<輸入任意詞開始挑禮物~>'
    messages0 = TextSendMessage(text=welcome_word0)
    #welcome_word1 = "歡迎來到「送禮達人」，我們的目標只有一個，就是為您找出讓人感動的禮物。\n\n我們每次會從不同角度協助您選擇，讓您每次都有不同的驚奇。"
    #messages1 = TextSendMessage(text=welcome_word1)
    #welcome_word2 = "請問您要送誰禮物？"
    #messages2 = TextSendMessage(text=welcome_word2)
    # call api 初始化使用者json檔(尚未打)
    line_bot_api.reply_message( event.reply_token, [messages0])


if __name__ == "__main__":
    # for heroku
    # app.run(host='0.0.0.0',port=os.environ['PORT'])

    # for localhost
    app.run(host='0.0.0.0')





