kitayama2bus=open("kitayama2nagao").readlines()
# print(kitayama2bus)
kitayama2bus=[int(i.replace("\n","")) for i in kitayama2bus]
# print(kitayama2bus)
nn=0x0A

import datetime
def getTime(week=True)->int:
    now = datetime.datetime.now()
    nowtime = now.hour * 100 + now.minute
    youbi=now.weekday() ## mon -> 0 tur ->1
    if week: return nowtime,youbi
    else: return nowtime
def now2Bus(format=True)->list:
    nowtime=getTime(False)
    ii=[i for i in kitayama2bus if nowtime<i]
    if format :return ii
    else: formatbus(ii)

def formatbus(time:list):
    ss=""
    for index,time in enumerate(time):
        time=str(time)
        time=time[:2]+":"+time[2::]
        print(time)
        if index==0:
            ss+=f"直近のバスは,{time}です。\n"
        else:
            ss+=f"{index+1}番目のバスは{time}です。\n"
        if index>=2:
            break
    return ss

import DataBase.zikanwari as zikan
def zikanwari(format=True):

    time,week=getTime()
    if week>=5: return "祝日くらい休みたい。"
    # week=1
    idx=[idx for idx,_ in enumerate(zikan.startTime) if time<=_][0]
    # idx=2

    ss=""
    for d in zikan.zikanwari[week][idx]:
        ss+=(d.replace(",","\n"))

    # print(zikan_zyugyou)
if __name__ == '__main__':
    # print(formatbus(now2Bus()))
    ss=zikanwari()
    print(ss)