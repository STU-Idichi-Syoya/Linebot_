from Line_Bot_Server.LineBot import line_bot_api

##### STATE #####


class LineUser:
    def __init__(self,reply=None,userId=None):
        '''line のユーザ情報クラス　ここではreplayからUserIdを取得することも
            できるし、そのままuserIdを入力できる。
            そこからLine APIを通して、名前と　ひとこと（status message）を取得する。
        '''

        #reply か　userIdどちらも情報がない場合,userIdはNone とする。
        if  (reply or userId):
            ##replyからuserIdを取得
            if reply:
                self.userId = reply.source.user_id
            else:
                self.userId=userId
            #replyから名前とひとことを取得
            profile = line_bot_api.get_profile(self.userId)
            self.status = (profile.status_message)
            self.name=profile.display_name
        else:
            self.userId=None
            self.name=None
            self.status=None

    def __eq__(self, other):
        if type(other)==LineUser:
            return self.userId == other.userId
        else:
            return self.userId== other

    def __str__(self):
        return f"userId::{self.userId}\n" \
            f"userName::{self.name}\n" \
            f"userStatus::{self.status}"


class LineSender:
    def __init__(self,lineins:LineBotApi):
        self.line_bot_api=lineins

    def sendMessage(self,text:str,user_id:LineUser):
        if isinstance(user_id,LineUser):
            user_id=user_id.userId
        msg=lineins.TextMessage(text=text)
        self.line_bot_api.push_message(to=user_id,messages=msg)


class LineUsers:
    def __init__(self):
        self.Users = {}

    def getState(self, user: LineUser):
        return self.Users[user.userId]
    def setState(self,user:LineUser,state):
        self.Users[user.userId]=state
    def __add__(self, other: LineUser):
        self.Users[other.userId] = other

    def __len__(self, other):
        return len(self.Users)
