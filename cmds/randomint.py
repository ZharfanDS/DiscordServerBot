# randomint.py
from discord.ext import commands

import random

# Random int choices
@commands.command(help='input random int ex; 1 2 5 6 (or more) the bot will choose')
async def choices(ctx, *options):
    await ctx.send(random.choice(options))

def setup(bot):
    bot.add_command(choices)