import discord
from discord.ext import commands, tasks
import json
from datetime import datetime, timedelta

file_path = "cogs\json_adzan\maret_adzan.json"

class BotNotifikasiPuasa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_prayer_times.start()

    @tasks.loop(seconds=60)
    async def check_prayer_times(self):
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%d %b %Y")
        channel_id = 1217086690615758889  # Replace with your desired channel ID
        channel = self.bot.get_channel(channel_id)
        time_notif_default = "02:21"
        today_timings = self.get_todays_ramadhan_prayer_times(current_date)

        if today_timings and current_time == time_notif_default:
            await channel.send(f"@everyone Jadwal Adzan Kota Bandung (Edisi Ramadhan 2024 / 1445 H) - {current_date}")
            if today_timings:
                await channel.send(f"Subuh: {today_timings['Fajr']},\nDzuhur: {today_timings['Dhuhr']},\nAshar: {today_timings['Asr']},\nMaghrib: {today_timings['Maghrib']},\nIsya: {today_timings['Isha']}.\nSumber : https://jadwal-imsakiyah.tirto.id/kota-bandung")
        
        time_str_subuh = today_timings['Fajr'][:5]
        time_obj = datetime.strptime(time_str_subuh, '%H:%M')
        time_obj_minus_2hour = time_obj - timedelta(hours=2)
        result_time_str = time_obj_minus_2hour.strftime('%H:%M')

        if today_timings and current_time == result_time_str:
            await channel.send("@everyone SAHUR!!! SAHUR!!! SAHUR!!!\nJangan lupa sahur untuk yang berpuasa!")

        if today_timings and current_time == today_timings["Maghrib"][:5]:
            await channel.send("SELAMAT BERBUKA PUASA BAGI YANG SEDANG BERPUASA! @everyone ^^")

    def get_todays_ramadhan_prayer_times(self, date):
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            
        for day_data in data["data"]:
            json_date = datetime.strptime(day_data["date"]["readable"], "%d %b %Y").strftime("%d %b %Y")
            if json_date == date:
                return day_data["timings"]
        return None

async def setup(bot):
    await bot.add_cog(BotNotifikasiPuasa(bot))
