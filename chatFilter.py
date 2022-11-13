from email.policy import default
import nextcord
from nextcord.ext import commands, tasks
from nextcord.utils import get
import string
import re
import json
from datetime import datetime, timedelta
import os
import random
import asyncio
import pymysql
import arrow
import money
import reinforce
import math



testcheck = open("secret/bootmode.txt", "r").read()

version="V-22-11-14-01"

sqlinfo = open("secret/mysql.json", "r")
sqlcon = json.load(sqlinfo)




server=""

if testcheck == "test":
    testmode = True
    server=sqlcon["test_server"]

elif testcheck == "main":
    testmode = False
    server=sqlcon["main_server"]
else:
    mode_error = open("errorinfo.txt", "w")
    mode_error.write("bootmode.txt의 내용이 'main'이거나 'test'가 아님")
    mode_error.close()

print(f"servername = {server}")

database = pymysql.connect(
    user=sqlcon["user"],
    host=server,
    database=sqlcon["db"],
    password=sqlcon["password"],
    charset=sqlcon["charset"],
    autocommit=True,
)


cur = database.cursor() # 쿼리 생성과 결과 조회를 위해 사용

intents = nextcord.Intents.all()
tokenfile = open("secret/token.json", "r", encoding="UTF-8")

bot = commands.Bot(command_prefix=["c!", "C!"], intents=intents)
daily_reboot=0

@bot.event
async def on_ready():
    print("bot login test")
    print(bot.user.name)
    print(bot.user.id)
    print("-----------")
    await bot.change_presence(
        status=nextcord.Status.online,
        activity=nextcord.Game(f"{now.year}-{now.month}-{now.day}의 {daily_reboot}번째 부팅"),
    )
    # bot.loop.create_task(job())


canspeak = None
cantalk = None


#음성채팅, 텍스트채팅
# async def job():

#     guild = await bot.fetch_guild(837200416303087616)
#     role = guild.default_role
#     perms = role.permissions

#     await CheckTimeAndManagePermission(role, perms)

#     while True:
#         await asyncio.sleep(60)
#         await CheckTimeAndManagePermission(role, perms)

#현재 작동하지 않는 시간에 따른 권한 제한
async def CheckTimeAndManagePermission(role, perms):
    global canspeak
    global cantalk

    currentTime=arrow.now('Asia/Seoul')

    currentTime = datetime.now()
    hour = currentTime.hour
    minute = currentTime.minute

    speak = None
    talk = None

    print(hour)
    print(minute)

    if (hour >= 2) and (hour < 6) and (canspeak == None or canspeak == True):
        print("speak off")
        perms.update(speak=False, connect=False)
        speak = 0
    elif (hour < 2) or (hour > 6) and (canspeak == None or canspeak == False):
        print("speak on")
        perms.update(speak=True, connect=True)
        speak = 1

    if (
        (hour >= 1 and minute >= 30)
        and (hour <= 5 and minute < 30)
        and (cantalk == None or cantalk == True)
    ):
        print("send message off")
        perms.update(send_messages=False)
        talk = 0
    elif ((hour <= 1 and minute < 30) or (hour >= 5 and minute >= 30)) and (
        cantalk == None or cantalk == False
    ):
        print("send message on")
        perms.update(send_messages=True)
        talk = 1

    if speak == 0:
        canspeak = False
    elif speak == 1:
        canspeak = True

    if talk == 0:
        cantalk = False
    else:
        cantalk = True

    await role.edit(permissions=perms)

#테스트 멤버가 나갔을때 입장테스트 DB 삭제



#멤버가 들어왔을때 입장테스트 DB 추가
@bot.event
async def on_member_join(member):

    channel = await member.guild.create_text_channel("입장채널")
    selfbot = nextcord.utils.get(member.guild.members, id=bot.user.id)

    await channel.set_permissions(member, read_messages=True)
    await channel.set_permissions(selfbot, read_messages=True)
    await channel.set_permissions(member.guild.default_role, read_messages=False)

    length=10

    testcode = random.sample(string.ascii_letters, length)

    teststring=""

    for i in testcode:
        teststring+=i

    sql=f"insert into entry_test values ({member.id},'{teststring}',{length})"
    cur.execute(sql)
    

    await channel.send(f"{testcode} 순서대로 채팅(1글자씩)")


async def CheckMessage(message):
    blackwordfile = open("secret/blackword.txt", "r", encoding="UTF-8")

    blackwordlist = blackwordfile.read().split("\n")
    blackwordfile.close()

    if message.author.bot:
        return

    if (
        ("?" in message.content or "？" in message.content)
        and message.content[0] == message.content[-1]
        and message.content[0] == "?"
        and len(message.content) > 3
    ):
        await message.delete()
        return

    fullmsg = message.content

    print("fullmsg   " + fullmsg)

    needDelete = None

    black_ctx = open("filt_ctx.txt", "w",encoding="UTF-8")
    black_ctx.write(message.content)
    black_ctx.close()

    for black in blackwordlist:

        if black in message.content:
            
            message.content = message.content.replace(black, "##")
            needDelete = True

    
    if needDelete:
        #user정보의 필터링 횟수를 확인


        #필터링 횟수에 플러스1



        #필터링횟수에 따른 타임아웃 적용




        #필터링 된 메세지 정보에 해당 유저의 필터링 횟수도 보여줌
        await message.delete()
        await message.channel.send(
            f"nick : {message.author.display_name}\n" + message.content
        )


@bot.event
async def on_message_edit(before, after):

    await CheckMessage(after)


@bot.event
async def on_message(tempmessage):

    if re.match("[A-z]{1}", tempmessage.content) and len(tempmessage.content) == 1:

        channelid = tempmessage.channel.id

        #입장테스트 유저 데이터를 불러옴
        sql=f"select test_string,remain_char from entry_test where discordid={tempmessage.author.id}"
        cur.execute(sql)

        entry_test_data=cur.fetchone()

        #입장 테스트 유저일때
        if entry_test_data!=None:
            remain_char=entry_test_data[2]

            if entry_test_data[1][10-remain_char]==tempmessage.content:

                
                #remain_char-1 DB에 반영

                #remain_chara-1 쿼리
                sql=f"update entry_test set remain_char=remain_char-1 where discordid={tempmessage.autuor.id}"


                #remain_chara-1 쿼리 실행
                cur.execute(sql)

                

                #입장테스트를 통과 했을때
                if len(entry_test_data['test_string']) == 0:
                    testrole = nextcord.utils.get(tempmessage.guild.roles, name="멤버")
                    await tempmessage.author.add_roles(testrole)


                    #entry_test db에서 멤버 행 삭제 쿼리
                    sql=f"delete from entry_test where discordid={tempmessage.author.id}"

                    #쿼리 실행
                    cur.execute(sql)


                    await bot.get_channel(channelid).delete()

                    #멤버 insert 쿼리
                    sql=f"insert into user (discordid) values ({tempmessage.author.id})"

                    #멤버 insert 쿼리 실행
                    cur.execute(sql)
                else:
                    await tempmessage.channel.send(f"{len(entry_test_data['test_string'])}자 남음")
            else:
                await tempmessage.channel.send("문자를 틀렸거나 관리자가 대신 입력 할 수 없습니다.")

    else:
        await CheckMessage(tempmessage)

        await bot.process_commands(tempmessage)

        if (
            tempmessage.author.bot
            or "C!" in tempmessage.content
            or "c!" in tempmessage.content
        ):
            return


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.emoji == "🖕":
        await reaction.remove(user)


chatStop = []

deleteCount = {}


tempvoice = False


@bot.command()
async def 상점(ctx,id):
    await ctx.send("준비중입니다. 11월 예정")
    return

    storedir=db.reference(f"{DBroot}/store")

    items=storedir.get()


    defaultstore={
        [
            {"name":"강화할수 있는 물건 +1","amount":200,"price":5000,"item_type":"can_reinforce_item"}
            ]
        }
    if id==None:
        if items==None:
            storedir.update(defaultstore)
            await ctx.send(defaultstore)
        else:
            await ctx.send(items)
    else:
        id=int(id)
        name=items[id-1]["name"]
        price=items[id-1]["price"]
        amount=items[id-1]["amount"]
        item_type=items[id-1]["item_type"]

        userdir=db.reference(f"{DBroot}/users/'{ctx.author.id}'")

        
        userinfo=userdir.get()

        if price>userinfo["money"]:
            await ctx.send(f"{price-userinfo['money']}money가 부족하여 {name} 구매 불가합니다.")
            return

        if "+" in name:
            name=name.split("+")

        if len(name)==2:
            if "inventory" in userinfo:
                if "can_reinforce_item" in userinfo["inventory"]:
                    if userinfo["inventory"]["can_reinforce_item"]==0:
                        userdir.update({"money":userinfo['money']-price,"inventory":{"can_reinforce_item":int(name[1])}})
                    else:
                        await ctx.send("강화할수 있는 물건을 이미 가지고 있습니다.")
                else:
                    userdir.update({"money":userinfo['money']-price,"inventory":{"can_reinforce_item":int(name[1])}})
            else:
                userdir.update({"money":userinfo['money']-price,"inventory":{"can_reinforce_item":int(name[1])}})
        else:
            await ctx.send("추후 구매 가능 예정")

        



@bot.command()
async def 강화(ctx):
    await ctx.send("준비중입니다. 11월 예정")
    return
    moneydir=db.reference(f"{DBroot}/users/'{ctx.author.id}'")

    reinforce.reinforce()

@bot.command()
async def 베팅(ctx,mode=None,amount=-50000):
    percent=0
    multiple=0

    
    amount=int(amount)

    sql=f"select money from users where discordid={ctx.author.id}"
    cur.execute(sql)
    havemoney=cur.fetchone()[0]

    if amount<=0 and mode!="7":
        await ctx.send("0money 이하 베팅 불가")
        return

    if mode=="1":
        percent=50
        multiple=2.2
    elif mode=="2":
        percent=30
        multiple=4
    elif mode=="3":
        percent=10
        multiple=12
    elif mode=="7":
        
        percent=40
        multiple=2.7
        amount=havemoney
    else:
        await ctx.send("잘못된 모드입력입니다.")
        return

    if havemoney<amount:
        await ctx.send(f"{amount-havemoney}모아가 부족합니다.")
        return


    sql=f"update users set money=money-{amount} where discordid={ctx.author.id}"
    print(sql)
    cur.execute(sql)

    dice=random.random()*100

    log=f"모드 {mode}를 사용하여 {percent}%로 {amount}모아를 {multiple}배 불리기 "

    if dice<percent:
        log+="성공함"
        sql=f"update users set money=money+{math.floor(amount*multiple)} where discordid={ctx.author.id}"
    else:
        log+="실패함"
    
    await ctx.send(log)
      
    sql=f"insert into log (discordid,version,command,discription) values ({ctx.author.id},'{version}','베팅','{log}')"

    cur.execute(sql)

@bot.command()
async def 출석(ctx):
    nowtime=arrow.now("Asia/Seoul")
    
    #제일 최근 출첵 날짜를 불러옴
    sql=f"select today_free_get from users where discordid={ctx.author.id}"

    cur.execute(sql)

    getdate=cur.fetchone()[0]

    tempbot_date=(arrow.now("Asia/Seoul").datetime-timedelta(hours=6)).date()

    print(tempbot_date)
    
    date_string=f"{tempbot_date.year}-{tempbot_date.month}-{tempbot_date.day}"

    #(현재시간 - 6시간)의 날짜와 획득날짜를 비교해서 같으면 return, 다르면 재화 지급
    if date_string!=getdate:
        result=money.dayget()

        sql=f"update users set money=money+{result[0]},today_free_get='{date_string}' where discordid={ctx.author.id}"
        cur.execute(sql)

        log=f"grade : {result[1]}, {result[0]}money 획득"

        await ctx.send(log)

        cur.execute(sql)

        

        sql=f"insert into log (discordid,version,command,discription) values ({ctx.author.id},'{version}','출석','{log}')"
        print(sql)
        cur.execute(sql)
    else:
        await ctx.send("이미 오늘은 얻었습니다. 리셋시간 : 오전6시")
        return

    
    

@bot.command()
async def 정보(ctx):

    sql=f"select point,activity_level,reinforce_level,money,today_free_get from users where discordid={ctx.author.id}"

    cur.execute(sql)

    result=cur.fetchone()
    
    await ctx.send(f"활동 포인트 : {result[0]}P\n활동 레벨 : {result[1]}레벨\n강화 레벨 : {result[2]}레벨\n{result[3]}모아 보유중\n마지막 출석 날짜 : {result[4]}")


@bot.command()
async def 제한음챗(ctx):
    global tempvoice

    limit = 300

    if not tempvoice:
        tempvoice = True
        cate = nextcord.utils.get(ctx.guild.categories, name="채팅 채널")
        chan = await ctx.guild.create_voice_channel(name=f"5분 음챗", category=cate)

        await asyncio.sleep(300)

        await chan.delete()
        tempvoice = False


# @bot.command()
# async def 뭐하지(ctx):
#     things = open("things.txt").readlines()
#     dolist = open("dolist.txt").readlines()
#     count = random.randrange(1, 11)

#     result1 = random.choice(things).replace("\n", "")
#     doresult = random.choice(dolist).replace("\n", "")

#     await ctx.send(f"{}으로 {} {}번 하기")


@bot.command()
async def 서버정보(ctx):

    await ctx.send(
        f"""
        서버 이름 : {ctx.guild.name}
        만들어진 시간 : {ctx.guild.created_at}(UTC)
        카테고리 개수 : {len(ctx.guild.categories)}
        텍스트 채널 개수 : {len(ctx.guild.text_channels)}
        음성채널 개수 : {len(ctx.guild.voice_channels)}
        스테이지 채널 개수 : {len(ctx.guild.stage_channels)}
        """
    )


@bot.command()
async def 등록(ctx):
    passid=968004898262220800

    users=ctx.guild.members

    regimember=[]

    for user in users:
        if not user.bot:
            if user.id!=passid:
                joindex=0
                for mem in regimember:
                    if user.joined_at > mem[1]:
                        joindex+=1
                
                regimember.insert(joindex,[user.id,user.joined_at])

    print(regimember)
    for mem in regimember:  
        sql=f"insert into user (discordid) values ({mem[0]})"
        cur.execute(sql)

@bot.command()
async def 집(ctx):
    now = datetime.now()

    limitDay = 4 - now.weekday()

    if limitDay < 0:
        await ctx.send("이미 집")
        return

    print(limitDay)

    homeTime = datetime(
        year=now.year, month=now.month, day=now.day, hour=7, minute=0, second=0
    ) + timedelta(days=limitDay)

    leave_time = homeTime - now

    limit_s = leave_time.seconds % 60
    limit_m = leave_time.seconds // 60 % 60
    limit_h = leave_time.seconds // 60 // 60

    if limitDay == 0 and now.hour >= 16 and leave_time.seconds > 8000:
        songlist = []
        with open("song.txt") as f:
            songlist = f.readlines()
        await ctx.send(random.choice(songlist))
    else:
        percent = 100 - (
            (
                (leave_time.days * 24 * 60 * 60 + limit_h * 60 * 60)
                + limit_m * 60
                + limit_s
            )
            / (112 * 60 * 60)
            * 100
        )

        progressbar = ""
        cut = 0
        rangecut = 40
        for i in range(rangecut):
            cut += 100 / rangecut
            if percent > cut:
                progressbar += "#"
            else:
                progressbar += "..."
        await ctx.send(
            f"""{'%.2f'%percent}% [{progressbar}]\n{leave_time.days}일 {limit_h}시간 {limit_m}분 {limit_s}초"""
        )


token = ""
if testmode:
    token = json.load(tokenfile)["testtoken"]
else:
    token = json.load(tokenfile)["token"]

now=arrow.now("Asia/Seoul")

if os.path.isfile(f"{now.year}{now.month}{now.day}"):
    mode_error = open(f"{now.year}{now.month}{now.day}", "r")
    daily_reboot=int(mode_error.read())
    mode_error.close()

    daily_reboot+=1
    
    mode_error = open(f"{now.year}{now.month}{now.day}", "w")
    mode_error.write(f"{daily_reboot}")
    mode_error.close()
else:
    mode_error = open(f"{now.year}{now.month}{now.day}", "w")
    mode_error.write("1")
    daily_reboot=1
    mode_error.close()


print(token)
bot.run(token)
