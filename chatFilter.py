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
import emoji
import pymysql
import arrow
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import money



testcheck = open("secret/bootmode.txt", "r").read()

cred = credentials.Certificate('secret/firebase-admin.json')
DBroot=""


sqlinfo = open("secret/firebase_url.json", "r")
sqlcon = json.load(sqlinfo)


if testcheck == "test":
    testmode = True
    DBroot="testDB"
    
elif testcheck == "main":
    testmode = False
    DBroot="mainDB"
else:
    mode_error = open("errorinfo.txt", "w")
    mode_error.write("bootmode.txt의 내용이 'main'이거나 'test'가 아님")
    mode_error.close()

firebase_admin.initialize_app(cred,{
    'databaseURL' : sqlcon["DBurl"]
})

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


async def job():

    guild = await bot.fetch_guild(837200416303087616)
    role = guild.default_role
    perms = role.permissions

    await CheckTimeAndManagePermission(role, perms)

    while True:
        await asyncio.sleep(60)
        await CheckTimeAndManagePermission(role, perms)


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



@bot.event
async def on_member_join(member):

    channel = await member.guild.create_text_channel("입장채널")
    selfbot = nextcord.utils.get(member.guild.members, id=bot.user.id)

    await channel.set_permissions(member, read_messages=True)
    await channel.set_permissions(selfbot, read_messages=True)
    await channel.set_permissions(member.guild.default_role, read_messages=False)


    testcode = random.sample(string.ascii_letters, 10)

    direct = db.reference(f"{DBroot}/entry_test/'{member.id}'")

    direct.update({"channelID":channel.id,"test_string":testcode})

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


        direct=db.reference(f"{DBroot}/entry_test/'{tempmessage.author.id}'")

        entry_test_data=direct.get()
        if entry_test_data!=None:
            if entry_test_data["test_string"][0]==tempmessage.content:
                print(entry_test_data)
                del entry_test_data["test_string"][0]
                print(entry_test_data)

                direct.update({"test_string":entry_test_data["test_string"]})

                await tempmessage.channel.send(f"{len(entry_test_data['test_string'])}자 남음")

                if len(entry_test_data['test_string']) == 0:


                    testrole = nextcord.utils.get(tempmessage.guild.roles, name="멤버")
                    await tempmessage.author.add_roles(testrole)

                    entry_test_dir=db.reference(f"{DBroot}/entry_test/'{tempmessage.author.id}'")

                    entry_test_dir.delete()


                    await bot.get_channel(channelid).delete()

                    entry_dir=db.reference(f"{DBroot}/users/'{tempmessage.author.id}'")

                    entry_dir.update({"point":0,"activity_level":1,"reinforce_level":1,"money":0})

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
async def 출석(ctx):
    nowtime=arrow.now("Asia/Seoul")
    
    moneydir=db.reference(f"{DBroot}/users/'{ctx.author.id}'")

    userdata=moneydir.get()
    print(f"userdata {userdata}")
    result=[]

    if "dayget" not in userdata:
        result=money.dayget(moneydir,userdata)
    else:
        if userdata["dayget"]!=f"{nowtime.date().year}-{nowtime.date().month}-{nowtime.date().day}":
            result=money.dayget(moneydir,userdata)
        else:
            await ctx.send("이미 오늘은 얻었습니다.")




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
async def 정보(ctx):

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

    for user in users:
        if not user.bot:
            if user.id!=passid:
                user_dir=db.reference(f"{DBroot}/users/'{user.id}'")
                user_dir.update({"point":0,"activity_level":1,"reinforce_level":1,"money":0})

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
