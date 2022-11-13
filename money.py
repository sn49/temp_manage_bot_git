import random
import arrow

def dayget():
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
    
    return getMoney,grade