import discord
from discord.ext import commands
from Music import Music
from Birthday import Birthday
from General import General
from ErrorHandler import CommandErrorHandler
from pytz import timezone
from datetime import datetime
import asyncio
import keep_alive
import os
from replit import db



intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='b!', intents=intents, help_command=None)
bot.add_cog(Music(bot))
bot.add_cog(Birthday(bot))
bot.add_cog(General(bot))
bot.add_cog(CommandErrorHandler(bot))
temp_disabled_command = bot.get_command("volume")
temp_disabled_command.enabled = False
tz = timezone("US/Eastern")

@bot.event
async def on_ready():
    print("Logged in as:\n{0.user.name}\n{0.user.id}".format(bot))

async def check_for_birthday():
    while True:
        now = datetime.now(tz)
        birthdays = db["birthdays"]
        if f"{now.month}/{now.day}" in birthdays:
            if now.hour == 8 and now.minute == 30:
                for guild in bot.guilds:
                    users_to_celebrate = []
                    for user_to_celebrate in birthdays[f"{now.month}/{now.day}"]:
                        if guild.get_member(int(user_to_celebrate)) is not None:
                            users_to_celebrate.append(user_to_celebrate)
                    if users_to_celebrate:
                        if discord.utils.get(guild.text_channels, name="birthdays") == None:
                            await guild.create_text_channel('birthdays')
                        channel = discord.utils.get(guild.channels, name="birthdays")
                        await channel.send("@everyone Hey guys! Today is a special day, it's the birthday of the following user(s)! : {}. Happy birthday!".format(" ".join([f"<@{int(user)}>" for user in users_to_celebrate])))
        if now.month == 12 and now.day == 25 and now.hour == 8 and now.minute == 30:
            for guild in bot.guilds:
                if discord.utils.get(guild.text_channels, name="birthdays") == None:
                    await guild.create_text_channel('birthdays')
                channel = discord.utils.get(guild.channels, name="birthdays")
                await channel.send("Merry Christmas @everyone ! Go spend time with your family! :>")
        await asyncio.sleep(60)

async def rate_limit_check():
    import requests

    r = requests.head(url="https://discord.com/api/v1")
    try:
        print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
    except:
        print("No rate limit")

BOTTOKEN = os.environ["BOTTOKEN"]

keep_alive.keep_alive()

bot.loop.create_task(check_for_birthday())
bot.loop.create_task(rate_limit_check())
bot.run(BOTTOKEN)
