from multiprocessing import Process

import config
import tweepy
from DataBase.timetimetime import DB_line
from flask import Flask, request, abort
from flask import redirect, render_template, flash
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, )

import Line_Bot_Server.LineUsers as LineUsers
from Line_Bot_Server.LineUsers import LineUser

####





DB_line = DB_line()

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN
CHANNEL_SECRET = config.LINE_CHANNEL_SECRET

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
sender=LineUsers.LineSender(line_bot_api)
GropeDict = {}
import queue

q = queue.Queue()

# @app.route("/")
# def hello_world():
#     return "THIS IS LINE BOT"

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

# import web_api.weather


userState={}
userId_tw={}
users=LineUsers.LineUsers()

import DataBase.DB_APPS_ORM as DB_APPS
import DataBase.timetimetime as timetimetime
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # group か　個人かを判定
    # isGroup = (event.source.type == "group")
    # print(isGroup)
    # print(event)
    user= LineUser(event)
    user_mes=event.message.text

    # DB_line.set_talk_history(user.userId,)
    state=DB_APPS.getState(user_id=user.userId)

    if (DB_APPS.existsUser(user.userId)):

        if "時間割通知y/n" in state and state["時間割通知y/n"]=="none":
           if ["y","n"] in user_mes:
            flag="Y" if "y" in user_mes else "N"
            state["時間割通知y/n"]=flag
            DB_APPS.setState(user.userId,state)
            sender.sendMessage("完了しました。後に、変更する場合、時間割変更と言ってください。",user)
            ##todo 時間割変更
           else:
               sender.sendMessage("y/nで入力してください。",user)
           # todo　教室変更
        if ["b","bus","バス","バ"] in user_mes:
            bustime=timetimetime.now2Bus(format=True)
            sender.sendMessage(bustime,user.userId)
            return
        elif ["時間","じ",] in user_mes:
            ss=timetimetime.zikanwari(True)
            sender.sendMessage(ss,user.userId)
            return




    else:
        sender.sendMessage("初追加ですね。データベースに保存しました。",user)
        sender.sendMessage("時間割を毎時間通知しますか？ -->y/n",user)
        state["時間割通知y/n"]="none"
        DB_APPS.AddUsers(user_id=user.userId,name=user.name)
        DB_APPS.setState(user.userId,state=state)


    DB_APPS.setTalkHistory(user.userId, talk=user_mes)






def q_put(q, msg):
    q.put(msg)






def _args():
    app.run(debug=False, host='0.0.0.0', port=5000)


def start():
    s = Process(target=_args)
    s.start()
    return q



if __name__ == "__main__":
    q = start()

    # # app.run(debug=True, host='0.0.0.0', port=5000)
    # userId="U8c8b0e06213c94bc4c7f42cac57cf1a7"
    # user=LineUser(userId=userId)
    # sender=LineSender(line_bot_api)



