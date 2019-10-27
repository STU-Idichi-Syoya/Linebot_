from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound




engin = create_engine("sqlite:///test.db")

base=declarative_base()


state_initFlag_dict={"init":"ok"}
state_initFlag_str="init:ok"
class DBLineUser(base):

    __tablename__="users"

    userid=Column(String(),primary_key=True)
    name=Column(String())
    state=Column(String(),default=state_initFlag_str)

    def __repr__(self):
        return f"DBLineUser(id={self.userid},name={self.name},inside_state={self.state}"

class DBTalkHistory(base):
    __tablename__="talkhistory"

    talkid=Column(Integer,autoincrement=True,primary_key=True)
    userid=Column(String())
    talk=Column(String())
    date=Column(Integer())

    def __repr__(self):
        return f"TALK_HIS(userid={self.userid} ,talkid={self.talkid},talk={self.talk})"

base.metadata.create_all(engin)

session=sessionmaker(bind=engin)
session=session()
### make LINE class###
# session.add(DBLineUser(userid="1",name="aho"))
# session.commit()
#
# session.add_all([ DBLineUser(userid=str(i),name=str(i)) for i in range(2,100)])
# session.commit()

### make talk class ###
# import time
# session.add_all([DBTalkHistory(userid=str(i),talk="ahoxsa",date=int(time.time())) for i in range(100)])
# session.commit()

import datetime,time
# for ins in session.query(DBTalkHistory).join(DBLineUser,DBLineUser.userid==DBTalkHistory.userid).filter(DBLineUser.userid==1):
#     print(datetime.datetime.fromtimestamp(ins.date),ins.talk)

def AddUsers(user_id:str,name="None"):
    session.add(DBLineUser(userid=user_id,name=name))
    session.commit()

def existsUser(user_id:str)->bool:
    query=session.query(DBLineUser).filter(DBLineUser.userid==user_id).all()

    return bool(query)
def setTalkHistory(user_id:str,talk:str,date:int=int(time.time())):
    session.add(DBTalkHistory(userid=user_id,talk=talk,date=date))

    session.commit()
import DataBase.State2PythonData as stringer

def getState(user_id:str)->dict:
    ss=session.query(DBLineUser.state).filter(DBLineUser.userid == user_id)[0][0]
    ss=stringer.State2Python(ss)
    return ss

def setState(user_id:str,state:dict):
    ss=stringer.dict2State(state)
    query=session.query(DBLineUser)
    user=query.filter(DBLineUser.userid==user_id).first()
    user.state=state
    # print(user)
    session.commit()
def getAlldata():
    return list(session.query(DBLineUser).all())
if __name__ == '__main__':
    # session.add(DBLineUser(userid="114514",name="aho"))
    # AddUsers(user_id="514514a",name="aho")
    # setState("514514", "111111")
    #
    # print(getState("514514"))
    #
    print(getAlldata())

    print(existsUser("514514a"))