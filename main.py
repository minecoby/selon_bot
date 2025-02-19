import discord
from discord.ext import commands
from variable import *
from database import *
from rss_feed import *
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='~', intents=intents, help_command=None)

notice_Base.metadata.create_all(bind=notice_engine)


@bot.event
async def on_ready():
    print(bot.user.name, '봇이 정상적으로 작동을 시작했습니다.')
    stat = discord.Game('코딩')
    await bot.change_presence(status=discord.Status.online, activity=stat)
    bot.loop.create_task(check_rss_feed(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  

    if message.channel.id == int(ASK_CHANNEL_ID): 
        await message.delete() 

        embed = discord.Embed(
            title="📌 질문",
            description=message.content,
            color=discord.Color.blue()  
        )
        await message.channel.send(embed=embed)
        
try:
    bot.run(bot_key)
except Exception as e:
    print(f"봇 실행 중 오류 발생: {e}")