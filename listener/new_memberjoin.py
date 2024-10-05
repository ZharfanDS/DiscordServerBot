# new_memberjoin.py
from discord.ext import commands

async def on_member_join(member):
    # Send a welcome message in DM
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.mention}, welcome to Discord server {member.guild.name}!'
        f'\nDon\'t forget to subscribe to my YouTube channel https://www.youtube.com/@ShirozID'
    )

    # Send a welcome message in the server channel
    guild = member.guild
    welcome_channel = guild.get_channel(1069772978113478676)  # Replace YOUR_WELCOME_CHANNEL_ID with the actual channel ID
    if welcome_channel:
        await welcome_channel.send(
            f'Hello {member.mention}, Welcome to Gamer Community discord server!'
            f'\nDon\'t forget to read {guild.get_channel(916033609209634876)} and select your roles at {guild.get_channel(865958511716204555).mention}.'
        )

def setup(bot):
    bot.add_listener(on_member_join)
