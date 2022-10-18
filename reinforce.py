import random

level = 1




try_count=0

#대충 랜덤 뭐시기로 30렙 될때까지 while문 돌린다는 내용
while level!=30:
    #확률 계산
    up4 = 0
    up2 = 0

    if level <= 25:
        up4 = 10 - 0.4 * (level - 1)
        up2 = up4 * 2
    elif level <= 27:
        up2 = 0.8 / (2 * (level - 25))
    up = 60 - 2 * (level - 1)

    down1 = 2 * (level - 1)

    destroy = 0

    if level >= 20:
        destroy += 0.1 * (level - 19)

    if level >= 10:
        destroy += 0.1 * (level - 9)

    destroy += 0.1 * level

    crack = destroy * 2

    notchange = 100 - up4 - up2 - up - down1 - crack - destroy


    # 확률 표기
    # print(f"level : {level}")
    # print(f"up4 : {up4}")
    # print(f"up2 : {up2}")
    # print(f"up : {up}")
    # print(f"notchange:{notchange}")
    # print(f"down1 : {down1}")
    # print(f"crack : {crack}")
    # print(f"destroy : {destroy}")

    res=random.random()*100




    print(f"{level}        {res}")


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
    elif res<up4+up2+up+notchange+down1+crack:

        #강화 불가 상태로 바꾸기

        #1~9 > 1레벨로, 10~19 > 10레벨로, 20>29 > 20레벨로(def fix .....으로 이동)
        if level<10:
            level=1
        elif level<20:
            level=10
        elif level<30:
            level=20
        
        
    elif res<up4+up2+up+notchange+down1+crack+destroy:
        level=1
    
    try_count+=1





#대충 총 트라이 횟수 알려주는 내용
print(try_count)