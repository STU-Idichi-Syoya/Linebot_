

def State2Python(state:str)->dict:
    ll=state.split(",")
    di={}
    for l in ll:
        l=l.split(":")
        di[l[0]]=l[1]

    return di
def dict2State(state:dict)->str:
    ll=["{","}","'"]
    ss=str(dict)
    for l in ll:
        ss=ss.replace(l,"")
        ss+=","
    if ss =="":
        return "None"
    return ss

if __name__ == '__main__':
    print(State2Python("init:ok,aho:ok"))