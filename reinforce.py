import random
import math
import copy
import numpy as np

level = 1


def getCost(level):
    return math.floor(1000**(1+0.03*level))*level

#대충 랜덤 뭐시기로 30렙 될때까지 while문 돌린다는 내용
def reinforce(level):

    #확률 계산
    up4 = 0
    up2 = 0
    down2=0
    down1=0

    if level <= 25:
        up4 = 10 - 0.4 * (level - 1)
        up2 = up4 * 2
    elif level <= 27:
        up2 = 0.8 / (2 * (level - 25))
    up = 60 - (level - 1)

    if level%5==0:
        down1=0
    else:
        down1 = (level - 1)

    destroy = 0

    if level >= 20:
        destroy += 0.1 * (level - 19)

    if level >= 10:
        destroy += 0.1 * (level - 9)

    if level>=3:
        if level%5==1:
            down2=0
        else:
            down2 = down1/2
        
        

    notchange = 100 - up4 - up2 - up - down1 - down2


    # 확률 표기
    # print(f"level : {level}")
    # print(f"up4 : {up4}")
    # print(f"up2 : {up2}")
    # print(f"up : {up}")
    # print(f"notchange:{notchange}")
    # print(f"down1 : {down1}")
    # print(f"down2 : {down2}")

    res=random.random()*100



    if res<up4:
        level+=4
    elif res<up4+up2:
        level+=2
    elif res<up4+up2+up:
        level+=1
    elif res<up4+up2+up+notchange:
        level+=0
    elif res<up4+up2+up+notchange+down1:
        level-=1
    elif res<up4+up2+up+notchange+down1+down2:
        level-=2
    
    return level



def reinTest():
    maxlevel=1
    count=0
    bonus=False
    complete=0
    countlist=np.array([])
    while complete!=1000000:
        complete+=1
        count=0
        level=1
        while level<30:
            level=reinforce(level)
            count+=1

            # if level%5==0:
            #     print(f"{count}회 현재레벨 : {level}")

            # if level>maxlevel:
            #     maxlevel=level
            #     print(f"{count}회 최대레벨 : {maxlevel}")
            #     bonus=not bonus
            #     continue

            


            if bonus:
                print(f"{count}회 현재레벨 : {level}")
                bonus=not bonus
        countlist = np.append(countlist, np.array([count]))
        if len(countlist)%10000==0:
            print(f"{countlist.shape[0]}회 평균 : {np.average(countlist)} 최대 : {np.max(countlist)} 최소 : {np.min(countlist)} 중앙값 : {np.median(countlist)}")
