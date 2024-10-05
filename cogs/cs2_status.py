import requests
import re
from discord.ext import commands

API_KEY = '266E82FA16920157C7E09BC89191F27B'
APP_ID = '730'  # Ganti dengan App ID CS2

# Fungsi untuk mendapatkan SteamID dari Vanity URL atau URL Profil Steam
def get_steam_id(profile_url):
    # Jika input adalah Steam Community Profile URL
    if "steamcommunity.com" in profile_url:
        steam_id_match = re.search(r"steamcommunity\.com/id/([^\/\s]+)", profile_url)
        if steam_id_match:
            custom_url = steam_id_match.group(1)
            url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={API_KEY}&vanityurl={custom_url}"
            response = requests.get(url).json()
            if response['response']['success'] == 1:
                return response['response']['steamid']
            else:
                return None
    # Jika input adalah Vanity URL
    else:
        url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={API_KEY}&vanityurl={profile_url}"
        response = requests.get(url).json()
        if response['response']['success'] == 1:
            return response['response']['steamid']
        else:
            return None

# Fungsi untuk mendapatkan informasi dasar pemain
def get_player_info(steam_id):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={API_KEY}&steamids={steam_id}"
    response = requests.get(url).json()
    if 'response' in response and 'players' in response['response'] and response['response']['players']:
        return response['response']['players'][0]
    else:
        return None

# Fungsi untuk mendapatkan statistik permainan CS2
def get_cs2_stats(steam_id):
    url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID}&key={API_KEY}&steamid={steam_id}"
    response = requests.get(url).json()
    # print("CS2 Stats Response:", response)  # Debug print
    if 'playerstats' in response and 'stats' in response['playerstats']:
        return response['playerstats']['stats']
    else:
        return None

# Fungsi untuk mengekstrak statistik yang relevan
def extract_relevant_stats(stats):
    relevant_stats = {}
    for stat in stats:
        if stat['name'] == 'total_kills':
            relevant_stats['Kills'] = stat['value']
        elif stat['name'] == 'total_deaths':
            relevant_stats['Deaths'] = stat['value']
        elif stat['name'] == 'total_wins':
            relevant_stats['Wins'] = stat['value']
        elif stat['name'] == 'total_rounds_played':
            relevant_stats['Rounds Played'] = stat['value']
        elif stat['name'] == 'total_kills_headshot':
            relevant_stats['Headshots'] = stat['value']
        elif stat['name'] == 'total_shots_fired':
            relevant_stats['Shots'] = stat['value']
    
    # Hitung statistik tambahan
    if 'Kills' in relevant_stats and 'Deaths' in relevant_stats:
        relevant_stats['K/D Ratio'] = relevant_stats['Kills'] / relevant_stats['Deaths']
    if 'Headshots' in relevant_stats and 'Kills' in relevant_stats:
        relevant_stats['Headshot Percentage'] = (relevant_stats['Headshots'] / relevant_stats['Kills']) * 100
    if 'Wins' in relevant_stats and 'Rounds Played' in relevant_stats:
        relevant_stats['Win Rate'] = (relevant_stats['Wins'] / relevant_stats['Rounds Played']) * 100

    print(relevant_stats)
    return relevant_stats

# Command untuk Discord bot
class CS2Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cs2info(self, ctx, vanity_url):
        steam_id = get_steam_id(vanity_url)
        if steam_id:
            player_info = get_player_info(steam_id)
            cs2_stats = get_cs2_stats(steam_id)
            if player_info and cs2_stats:
                player_name = player_info.get('personaname', 'Unknown')
                await ctx.reply(f"Informasi Pemain: {player_name}")
                
                relevant_stats = extract_relevant_stats(cs2_stats)
                stats_message = "\n".join([
                    f"🔥 Kills : {relevant_stats.get('Kills', 0)} 🔥",
                    f"☠️ Deaths : {relevant_stats.get('Deaths', 0)} ☠️",
                    f"💥 Wins : {relevant_stats.get('Wins', 0)} 💥",
                    f"⚔️ Rounds Played : {relevant_stats.get('Rounds Played', 0)} ⚔️",
                    f"🤯 Headshots : {relevant_stats.get('Headshots', 0)} 🤯",
                    f"🔫 Shots : {relevant_stats.get('Shots', 0)} 🔫",
                    f"⚔️ K/D Ratio : {relevant_stats.get('K/D Ratio', 0):.2f} ⚔️",
                    f"🤯 Headshot Percentage : {relevant_stats.get('Headshot Percentage', 0):.2f}% 🤯",
                    f"🏆 Win Rate : {relevant_stats.get('Win Rate', 0):.2f}% 🏆"
                ])
                
                await ctx.reply(f"Statistik CS2:\n{stats_message}")
            else:
                await ctx.reply("Tidak dapat menemukan informasi pemain atau statistik CS2.")
        else:
            await ctx.reply("Steam ID tidak ditemukan.")


async def setup(bot):
    await bot.add_cog(CS2Info(bot))
