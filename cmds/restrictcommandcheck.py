# import discord
# from discord.ext import commands

# def is_owner(ctx):
#     return ctx.message.author.id == 440514731380441091

# @commands.command()
# @commands.check(is_owner)
# async def say(ctx, what="WHAT"):
#     await ctx.send(what)

# @say.error
# async def say_error(ctx, error):
#     if isinstance(error, commands.CheckFailure):
#         await ctx.send("Permission Denied.")

# async def setup(bot):
#     await bot.add_command(say)