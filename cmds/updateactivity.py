# updateactivity.py
import discord
import datetime as dt
import asyncio
import pytz
from tzlocal import get_localzone

async def update_activity(bot):
    channel_id = 1184745606326001717  # Replace with your actual channel ID

    while True:
        # Get the local time zone
        local_tz = get_localzone()

        # Convert local time to West Indonesia Time, Central Indonesia Time, and East Indonesia Time
        wib_time = dt.datetime.now(local_tz).astimezone(pytz.timezone('Asia/Jakarta')).strftime('%d/%m %H:%M ')
        wita_time = dt.datetime.now(local_tz).astimezone(pytz.timezone('Asia/Makassar')).strftime('%d/%m %H:%M ')
        wit_time = dt.datetime.now(local_tz).astimezone(pytz.timezone('Asia/Jayapura')).strftime('%d/%m %H:%M ')
        await bot.change_presence(activity=discord.Game(name=f"🕗: {wib_time} WIB"))
        await asyncio.sleep(20)
        await bot.change_presence(activity=discord.Game(name=f"🕗: {wita_time} WITA"))
        await asyncio.sleep(20)
        await bot.change_presence(activity=discord.Game(name=f"🕗: {wit_time} WIT"))
        await asyncio.sleep(20)
