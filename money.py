import random
import arrow

def dayget():
    res=random.random()*100

    getMoney=0
    grade=0

    if res<40:
        getMoney=random.randint(10000,100000)
        grade=1
    elif res<70:
        getMoney=random.randint(40000,110000)
        grade=2
    elif res<90:
        getMoney=random.randint(80000,130000)
        grade=3
    else:
        getMoney=random.randint(130000,160000)
        grade=4
    
    return getMoney,grade