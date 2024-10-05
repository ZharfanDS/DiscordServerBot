from discord.ext import commands
import re

class Reporting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.report_command_pattern = re.compile(r'^!report\b', re.IGNORECASE)

    @commands.command(name='report')  
    async def report_anything(self, ctx, *, pesan: str):
        try:
            bot_owner = self.bot.get_user(440514731380441091)
            if bot_owner:
                await bot_owner.send(f"***Laporan Umum dari {ctx.author.name} ({ctx.author.id}) di Server {ctx.guild.name} ({ctx.guild.id}):***\n{pesan}")
            else:
                await ctx.send("***Gagal mengirim laporan kepada pemilik bot.***")
        except Exception as e:
            await ctx.send(f"***Terjadi kesalahan saat mengirim laporan:***\n{str(e)}")

    @commands.Cog.listener()
    async def on_message(self, message):
        # if message.content.startswith('!report'):
        if self.report_command_pattern.search(message.content):
            # Reply directly to the user's message
            await message.reply("***Laporan Umum Telah Dikirim kepada Pemilik Bot!***")

async def setup(bot):
    await bot.add_cog(Reporting(bot))
