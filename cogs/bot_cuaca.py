import discord
from discord.ext import commands, tasks
import requests
import datetime
import pyttsx3

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "6d3f5941dc27e5b3a87709a670bfb855"  # Replace with your Weatherstack API key
        self.target_channel_id = 1195678459058471013  # Replace with your target channel ID

        # Set the desired times to send weather data
        self.send_times = ["06:00", "15:00"]  #"09:00", "12:00", "15:00", "18:00", "21:00", "00:00", "03:00"]

        # Start the background task
        self.send_weather_task.start()

    def cog_unload(self):
        # Stop the background task when the cog is unloaded
        self.send_weather_task.cancel()

    @tasks.loop(minutes=1)  # Check every minute
    async def send_weather_task(self):
        now = datetime.datetime.now().strftime("%H:%M")

        if now in self.send_times:
            # Replace "YourCity" with the default city you want to get weather for
            default_city = "Bandung, West Java, Indonesia"
            await self.send_weather_data(default_city)

    async def send_weather_data(self, city):
        base_url = f"http://api.weatherstack.com/current?access_key={self.api_key}&query={city}"

        try:
            response = requests.get(base_url)
            data = response.json()

            if "error" in data:
                raise Exception(data["error"]["info"])

            temperature = data["current"]["temperature"]
            weather_description = data["current"]["weather_descriptions"][0]
            humidity = data["current"]["humidity"]

            # Menetapkan nilai default untuk deskripsi_cuaca
            deskripsi_cuaca = ""  # Nilai default

            #1
            if weather_description == "Clear":
                deskripsi_cuaca = "Cerah"
            #2
            elif weather_description == "Overcast":
                deskripsi_cuaca = "Mendung"
            #3
            elif weather_description == "Light rain":
                deskripsi_cuaca = "Hujan ringan"
            #4
            elif weather_description == "Heavy Rain":
                deskripsi_cuaca = "Hujan deras"
            #5
            elif weather_description == "Thunderstorm":
                deskripsi_cuaca = "Hujan badai"
            #6
            elif weather_description == "Snow":
                deskripsi_cuaca = "Bersalju"
            #7
            elif weather_description == "Fog":
                deskripsi_cuaca = "Berkabut"
            #8
            elif weather_description == "Mist":
                deskripsi_cuaca = "Berkabut"
            #9
            elif weather_description == "Smoke":
                deskripsi_cuaca = "Berasap atau berkabut"
            #10
            elif weather_description == "Sunny":
                deskripsi_cuaca = "Cerah"
            #11
            elif weather_description == "Cloudy":
                deskripsi_cuaca = "Berawan"
            #12
            elif weather_description == "Patchy rain possible":
                deskripsi_cuaca = "Kemungkinan terjadi hujan ringan"
            #13
            elif weather_description == "Patchy snow possible":
                deskripsi_cuaca = "Kemungkinan turun salju tidak merata"
            #14
            elif weather_description == "Patchy sleet possible":
                deskripsi_cuaca = "Kemungkinan terjadi hujan es yang tidak merata"
            #15
            elif weather_description == "Patchy freezing drizzle possible":
                deskripsi_cuaca = "Kemungkinan ada gerimis yang tidak merata"
            #16
            elif weather_description == "Thundery outbreaks possible":
                deskripsi_cuaca = "Kemungkinan ada wabah yang terjadi"
            #17
            elif weather_description == "Blowing snow":
                deskripsi_cuaca = "Hembusan salju"
            #18
            elif weather_description == "Blizzard":
                deskripsi_cuaca = "Badai salju"
            #19
            elif weather_description == "Freezing fog":
                deskripsi_cuaca = "Kabut yang membekukan"
            #20
            elif weather_description == "Patchy light drizzle":
                deskripsi_cuaca = "Gerimis tipis-tipis"
            #21
            elif weather_description == "Light drizzle":
                deskripsi_cuaca = "Gerimis ringan"
            #22
            elif weather_description == "Freezing drizzle":
                deskripsi_cuaca = "Gerimis yang membekukan"
            #23
            elif weather_description == "Heavy freezing drizzle":
                deskripsi_cuaca = "Gerimis yang sangat dingin"
            #24
            elif weather_description == "Patchy light rain":
                deskripsi_cuaca = "Hujan ringan yang tidak merata"
            #25
            elif weather_description == "Moderate rain at times":
                deskripsi_cuaca = "Terkadang hujan sedang"
            #26
            elif weather_description == "Moderate rain":
                deskripsi_cuaca = "Hujan sedang"
            #27
            elif weather_description == "Heavy rain at times":
                deskripsi_cuaca = "Kadang-kadang terjadi hujan lebat"
            #28
            elif weather_description == "Light freezing rain":
                deskripsi_cuaca = "Hujan ringan yang membekukan"
            #29
            elif weather_description == "Haze":
                deskripsi_cuaca = "Berkabut"
            #30
            elif weather_description == "Light rain shower":
                deskripsi_cuaca = "Hujan ringan"
            #31
            elif weather_description == "Patchy rain nearby":
                deskripsi_cuaca = "Hujan merata disekitar"
            #32
            elif weather_description == "Partly Cloudy":
                deskripsi_cuaca = "Sebagaian Berawan"
            #33
            elif weather_description == "Moderate or heavy rain in area with thunder":
                deskripsi_cuaca = "Hujan sedang atau lebat di daerah yang disertai petir"

            # Send the response to the specific channel
            channel = self.bot.get_channel(self.target_channel_id)
            await channel.send(f"***=== Weather Information ===\nCuaca | Weather - {city}: {deskripsi_cuaca} | {weather_description}\nTemperatur | Temperature: {temperature}°C\nKelembaban | Humidity: {humidity}%\nYou can use '!cuaca (input city or location)' to check weather by user input.***")
        except Exception as e:
            print(f"Terjadi kesalahan saat mengambil data cuaca untuk {city}: {e}")

    @commands.command(name='cuaca')
    async def get_cuaca(self, ctx, *, city: str):
        await self.send_weather_data(city)

    @commands.command(name='weather')
    async def get_weather(self, ctx, *, city: str):
        await self.send_weather_data(city)

async def setup(bot):
    await bot.add_cog(WeatherCog(bot))
