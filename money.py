import random
import arrow

def dayget(moneydir,userdata):
    nowtime=arrow.now("Asia/Seoul")

    res=random.random()*100

    getMoney=0
    grade=0

    if res<40:
        getMoney=random.randint(1000,10000)
        grade=1
    elif res<70:
        getMoney=random.randint(4000,11000)
        grade=2
    elif res<90:
        getMoney=random.randint(8000,13000)
        grade=3
    else:
        getMoney=random.randint(13000,16000)
        grade=4
    print(f"moneydir : {moneydir}")
    
    moneydir.update(
        {"dayget":f"{nowtime.date().year}-{nowtime.date().month}-{nowtime.date().day}",
        "money":userdata["money"]+getMoney}
        )
    gradecount=[0,0,0,0]
    if "stat" not in userdata:
        gradecount[grade-1]+=1
        moneydir.update({"stat":{"dayget":{"countdays":1,"gradeCount":gradecount,"totalDayGet":getMoney}}})
    else:
        if "dayget" not in userdata["stat"]:
            moneydir.update({"stat":{"dayget":{"countdays":1,"gradeCount":gradecount,"totalDayGet":getMoney}}})
        else:
            statdata=userdata["stat"]["dayget"]

            gradecount=statdata["gradeCount"]
            gradecount[grade-1]+=1

            moneydir.update({"stat":{"dayget":{"countdays":statdata["countdays"]+1,"gradeCount":gradecount,"totalDayGet":statdata["totalDayGet"]+getMoney}}})



    return getMoney,grade