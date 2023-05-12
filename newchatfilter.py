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
import traceback
import copy

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def returnNow():
    return arrow.now("Asia/Seoul")
owner= int(open("secret/ownerid.txt", "r").read())
maintence=False
testcheck = open("secret/bootmode.txt", "r").read()

version="V2-23-03-02-01"

sqlinfo = open("secret/mysql.json", "r")
sqlcon = json.load(sqlinfo)
bot_pause=False

intents = nextcord.Intents.all()
tokenfile = open("secret/token.json", "r", encoding="UTF-8")

bot = commands.Bot(command_prefix=["c!", "C!"], intents=intents)
daily_reboot=0

token = json.load(tokenfile)

# Fetch the service account key JSON file contents
cred = credentials.Certificate('secret/firebase-admin.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': token["firebase-url"]
})
testmode=True
DBroot=""
if testcheck == "test":
    testmode = True
    DBroot="testDB"
elif testcheck == "main":
    testmode = False
    DBroot="mainDB"

@bot.event
async def on_ready():
    channel=int(open("secret/channelid.txt","r").read())
    channel=bot.get_channel(channel)
    print("bot login test")
    print(bot.user.name)
    print(bot.user.id)
    print("-----------")
    now=returnNow()
    await bot.change_presence(
        status=nextcord.Status.online,
        activity=nextcord.Game(f"{now.year}-{now.month}-{now.day}의 {daily_reboot}번째 부팅, 현재 버전 : {version}"),
    )
    await channel.send("템프 관리 봇 켜짐")

async def CheckMessage(message):
    blackwordfile = open("secret/blackword.txt", "r", encoding="UTF-8")

    blackwordlist = blackwordfile.read().split("\n")
    blackwordfile.close()

    if message.author.bot:
        return

    fullmsg = message.content

    print("fullmsg   " + fullmsg)

    needDelete = None

    black_ctx = open("filt_ctx.txt", "w",encoding="UTF-8")
    black_ctx.write(message.content)
    black_ctx.close()

    newmsg=message.content.replace(" ","")

    for black in blackwordlist:

        if black in newmsg:
            
            newmsg = newmsg.replace(black, "## ")
            needDelete = True

    
    if needDelete:
        #user정보의 필터링 횟수를 확인



        #필터링 횟수에 플러스1




        #필터링횟수에 따른 타임아웃 적용




        #필터링 된 메세지 정보에 해당 유저의 필터링 횟수도 보여줌
        await message.delete()
        await message.channel.send(
            f"nick : {message.author.display_name}\n" + newmsg
        )

@bot.event
async def on_message(tempmessage):
    data=db.reference(f'{DBroot}/entry_test/{tempmessage.author.id}').get()

    print(data)

    if data!=None:
        answer=token["answer"]
        user_ans=str(tempmessage.content).replace(" ","")
        user_ans=user_ans.lower()

        print(user_ans)
        print(answer)

        if user_ans in answer:
            channel=bot.get_channel(int(data['channel_id']))

            testrole = nextcord.utils.get(tempmessage.guild.roles, name="멤버")
            await tempmessage.author.add_roles(testrole)

            entry_test_dir=db.reference(f"{DBroot}/entry_test/'{tempmessage.author.id}'")

            entry_test_dir.delete()

            user_dir=db.reference(f"{DBroot}/users/'{tempmessage.author.id}'")

            now=returnNow()
            user_dir.update({"Competition_Stack":1,"free_get":f"{now.year}{now.month}{now.day}"})

            await channel.delete()


    await CheckMessage(tempmessage)
    await bot.process_commands(tempmessage)

@bot.command()
async def 정보(ctx):
    user_dir=db.reference(f"{DBroot}/users/'{ctx.author.id}'")
    data=user_dir.get()
    await ctx.send(data)

@bot.command()
async def 닉네임(ctx,id):
    user=bot.get_user(int(id))
    await ctx.send(user.display_name)


@bot.command()
async def 대회지급(ctx,id,amount):
    
    if ctx.author.id==owner:
        if amount==None:
            await ctx.send("양 입력")
            return
        user_dir=db.reference(f"{DBroot}/users/'{id}'")
        data=user_dir.get()
        user_dir.update({"Competition_Stack":data["Competition_Stack"]+int(amount)})
        await ctx.send("지급 완료")



# @bot.command()
# async def 모두등록(ctx):
#     users=ctx.guild.members

#     for user in users:
#         if not user.bot:
#             user_dir=db.reference(f"{DBroot}/users/'{user.id}'")
#             user_dir.update({"Competition_Stack":0,"free_get":f"X"})

@bot.command()
async def 출석(ctx):
    user_dir=db.reference(f"{DBroot}/users/'{ctx.author.id}'")
    data=user_dir.get()

    now=returnNow()
    print(data)

    if data["free_get"]!=f"{now.year}{now.month}{now.day}" or data["free_get"]=="X":
        user_dir.update({"Competition_Stack":data["Competition_Stack"]+1,"free_get":f"{now.year}{now.month}{now.day}"})
        await ctx.send("출석완료")

    else:
        await ctx.send("오늘은 이미 출첵함")

@bot.event
async def on_member_join(member):

    channel = await member.guild.create_text_channel("입장채널")
    selfbot = nextcord.utils.get(member.guild.members, id=bot.user.id)

    await channel.set_permissions(selfbot, read_messages=True)
    await channel.set_permissions(member, read_messages=True)
    await channel.set_permissions(member.guild.default_role, read_messages=False)

    
    #firebase entry_test에 등록
    ref=db.reference(f"{DBroot}/entry_test/{member.id}")
    ref.update({"channel_id":f"{channel.id}"})
    

    await channel.send(token["question"])



if testmode:
    bot.run(token["testtoken"])
else:
    bot.run(token["token"])