 import os
import discord
from discord.ext import commands
import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# スケジュールをグローバルスコープに移動
even_schedule = {
    0: "エリジウムアンテナ",
    1: "リベリオンキャノン",
    2: "アストラアンテナ",
    3: "アストラキャノン",
    4: "リベリオンアンテナ",
    5: "覇者キャノン",
    6: "覇者アンテナ",
    7: "アオイキャノン",
    8: "アオイアンテナ",
    9: "リベリオンキャノン",
    10: "エリジウムアンテナ",
    11: "アストラキャノン",
    12: "アストラアンテナ",
    13: "覇者キャノン",
    14: "リベリオンアンテナ",
    15: "アオイキャノン",
    16: "覇者キャノン",
    17: "アオイアンテナ",
    18: "アオイキャノン",
    19: "エリジウムアンテナ",
    20: "リベリオンキャノン",
    21: "アストラアンテナ",
    22: "アストラキャノン",
    23: "リベリオンアンテナ"
}

odd_schedule = {
    0: "覇者キャノン",
    1: "覇者アンテナ",
    2: "アオイキャノン",
    3: "アオイアンテナ",
    4: "リベリオンキャノン",
    5: "エリジウムアンテナ",
    6: "アストラキャノン",
    7: "アストラアンテナ",
    8: "覇者キャノン",
    9: "リベリオンアンテナ",
    10: "アオイキャノン",
    11: "覇者アンテナ",
    12: "リベリオンキャノン",
    13: "アオイアンテナ",
    14: "アストラキャノン",
    15: "エリジウムアンテナ",
    16: "アストラアンテナ",
    17: "リベリオンキャノン",
    18: "リベリオンアンテナ",
    19: "アストラキャノン",
    20: "覇者アンテナ",
    21: "覇者キャノン",
    22: "アオイアンテナ",
    23: "アオイキャノン"
}

def get_response(hour, is_even_day):
    return even_schedule[hour] if is_even_day else odd_schedule[hour]

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)
    
@bot.command()
async def now(ctx):
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    current_hour = now.hour
    is_even_day = now.day % 2 == 0
    response = get_response(current_hour, is_even_day)
    await ctx.send(response)

@bot.command()
async def next(ctx):
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    next_hour = (now + datetime.timedelta(hours=1))
    is_even_day = next_hour.day % 2 == 0
    response = get_response(next_hour.hour, is_even_day)
    await ctx.send(response)

@bot.command()
async def when(ctx, *, search_term):
    even_times = [f"{hour}時" for hour, place in even_schedule.items() if search_term in place]
    odd_times = [f"{hour}時" for hour, place in odd_schedule.items() if search_term in place]
    
    if not even_times and not odd_times:
        await ctx.send("指定された場所は見つかりませんでした。")
        return
        
    response = f"**{search_term}** の時間帯:\n"
    if even_times:
        response += "偶数日: " + ", ".join(even_times) + "\n"
    if odd_times:
        response += "奇数日: " + ", ".join(odd_times)
    
    await ctx.send(response)

try:
    token = os.getenv("TOKEN")
    if not token:
        raise Exception("Please add your token to the Secrets pane.")
    print("Starting bot with token...")
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        print(f"HTTP Exception: {e}")
except Exception as e:
    print(f"Error: {e}")
