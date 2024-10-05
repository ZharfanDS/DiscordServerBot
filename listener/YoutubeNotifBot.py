import discord
from discord.ext import commands

class YoutubeNotifBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Pastikan bot tidak merespon pesan dari dirinya sendiri
        if message.author == self.bot.user:
            return

        # Cek apakah pesan mengandung link YouTube live
        if "https://youtube.com/live/" in message.content or "https://www.youtube.com/live/" in message.content:
            # Mention everyone dan balas pesan
            await message.reply(f"@everyone {message.author.mention} just shared Youtube Livestream link!", mention_author=False)
        
        elif "https://youtube.com/shorts" in message.content:
            await message.reply(f"@everyone {message.author.mention} just shared Youtube Shorts Video link!", mention_author=False)
        
        elif "https://youtu.be/" in message.content:
            await message.reply(f"@everyone {message.author.mention} just shared Youtube Video link!", mention_author=False)

# Setup cog
async def setup(bot):
    await bot.add_cog(YoutubeNotifBot(bot))