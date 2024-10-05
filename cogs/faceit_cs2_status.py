import discord
from discord.ext import commands
import requests
import os

FACEIT_API_KEY = '383ef526-8b14-4cf7-bd6b-cf2b2cb1bbe2'

class FaceitStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='faceit_cs2_status')
    async def status(self, ctx, *, username: str):
        headers = {
            'Authorization': f'Bearer {FACEIT_API_KEY}'
        }
        params = {
            'nickname': username,
            'game': 'cs2'
        }
        
        response = requests.get(f"https://open.faceit.com/data/v4/players", headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            # Contoh: Menampilkan hanya beberapa informasi
            info = f"Player: {data['nickname']}\nLevel: {data['games']['cs2']['skill_level']}\nELO: {data['games']['cs2']['faceit_elo']}"
            await ctx.send(info)
        else:
            await ctx.send(f"Player {username} tidak ditemukan atau terjadi kesalahan.")

async def setup(bot):
    await bot.add_cog(FaceitStatus(bot))
