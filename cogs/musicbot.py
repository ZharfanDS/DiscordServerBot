import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
import re
import discord.opus

import sys
sys.stdout.reconfigure(encoding='utf-8')

opus_path = r'D:\Program (Software)\Visual Studio Code CODE\discord-bot\shiroz\discordopus\opusfile-0.12_2\opusfile-0.12\win32\libopus-0/libopus-0.dll'
discord.opus.load_opus(opus_path)

if not discord.opus.is_loaded():
    discord.opus.load_opus(r'D:\Program (Software)\Visual Studio Code CODE\discord-bot\shiroz\discordopus\opusfile-0.12_2\opusfile-0.12\win32\libopus-0/libopus-0.dll')

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        ytdl = yt_dlp.YoutubeDL()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return filename, data

# Music commands
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.is_playing = False
        self.is_paused = False
        self.play_command_pattern = re.compile(r'^!play https:', re.IGNORECASE)
        self.play_command_pattern2 = re.compile(r'^!play https:', re.IGNORECASE)
        self.show_queue_command_pattern = re.compile(r'^!queue', re.IGNORECASE)
        self.pause_command_pattern = re.compile(r'^!pause', re.IGNORECASE)
        self.resume_command_pattern = re.compile(r'^!resume', re.IGNORECASE)

    async def delete_all_music_files(self):
    # Specify the folder where your mp4 files are stored
        # music_folder = "D:\\Program (Software)\\Visual Studio Code CODE\\discord-bot\\shiroz" # Delete # for release code
        music_folder = "D:\\Program (Software)\\Visual Studio Code CODE\\discord-bot\\shiroz\\dist" #Delete #for exe file
        # music_folder = "D:\\Program (Software)\\Visual Studio Code CODE\\discord-bot" #Delete # for debugging
        
        # Delete only mp4 files in the folder
        for filename in os.listdir(music_folder):
            file_path = os.path.join(music_folder, filename)
            print(f"Checking file: {file_path}")
            try:
                # Check if the file is an mp4 file
                if os.path.isfile(file_path) and filename.endswith(".mp4") or filename.endswith(".webm") or filename.endswith(".mkv"):
                    print(f"Deleting file: {file_path}")
                    os.unlink(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
                
        # # Delete only mp4 files in the folder
        # for filename in os.listdir(music_folder):
        #     file_path = os.path.join(music_folder, filename)
        #     try:
        #         # Check if the file is an mp4 file
        #         if os.path.isfile(file_path) and filename.endswith(".mp4"):
        #             os.unlink(file_path)
        #     except Exception as e:
        #         print(f"Error deleting file {file_path}: {e}")

    async def play_next(self, ctx):
        # Check if there are no more songs in the queue but still playing the last one
        if not self.queue and not ctx.voice_client.is_playing():
            self.is_playing = False  # Set is_playing to False before disconnecting
            if ctx.voice_client:
                await ctx.send('***No song left in the queue...***')
                await self.delete_all_music_files()
                await ctx.voice_client.disconnect()
            return

        # Check if the bot is connected to a voice channel
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            # Connect to the author's voice channel
            await ctx.author.voice.channel.connect()

        self.is_playing = True
        url, data = self.queue.pop(0)

        async with ctx.typing():
            filename, _ = await YTDLSource.from_url(url, loop=self.bot.loop)
            print(f'Attempting to play: {filename.split("[")[0].strip()}')
            await ctx.send(f'***Playing Song :*** {filename.split("[")[0].strip()}\n***You can input a command***\n| *!play* | *!next* | *!queue* | *!pause* | *!resume* | *etc*')
            
            def after_playing(e):
                self.is_playing = False
                self.bot.loop.create_task(self.play_next(ctx))
            
            # Define FFmpeg options as a string
            ffmpeg_options = "-b:a 256k -vn"

            ctx.voice_client.play(
                discord.FFmpegPCMAudio(
                    executable="D:\\Program (Software)\\Visual Studio Code CODE\\discord-bot\\shiroz\\youtubemusic\\ffmpeg-6.1-full_build\\bin\\ffmpeg.exe",
                    source=filename,
                    options=ffmpeg_options
                ),
                after=after_playing
            )
            print('Audio playback initiated.')

        # Check if there is still at least one more song in the queue after playing the current one
        if not self.queue and not ctx.voice_client.is_playing():
            await self.delete_all_music_files()
            await ctx.voice_client.disconnect()

    async def play(self, ctx, url):
        # Check if the user is in a voice channel
        if not ctx.author.voice or not ctx.author.voice.channel:
            print("Your bot is not inside the voice channel!")
            await ctx.send("***You need to be in a voice channel to use this command, Please Try Again.***")
            return

        # Check if the bot is already in a voice channel
        if ctx.voice_client and ctx.voice_client.is_connected():
            # If the bot is in a different channel, move to the author's channel
            if ctx.voice_client.channel.id != ctx.author.voice.channel.id:
                await ctx.voice_client.move_to(ctx.author.voice.channel)
        else:
            # If not in a voice channel, connect to the author's channel
            await ctx.author.voice.channel.connect()

        # Rest of the code for playing the song
        self.queue.append((url, await YTDLSource.from_url(url, loop=self.bot.loop)))
        print('SONG ARE ADDED TO QUEUE!')

        # If not currently playing, start playing the next song
        if not self.is_playing:
            await self.play_next(ctx)

        # If the queue is empty, set up an event to disconnect the bot when playback ends
        if not self.queue and not self.is_playing:
            await self.delete_all_music_files()
            await ctx.voice_client.disconnect()

    @commands.command(name='resume', help='Resume the music playback.')
    async def resume_command(self, ctx):
        if ctx.voice_client and not ctx.voice_client.is_playing() and self.is_paused:
            ctx.voice_client.resume()
            self.is_paused = False
            await self.display_resume(ctx.message)
    
    async def on_message(self, message):
        if self.resume_command_pattern.search(message.content):
            await self.display_resume(message)

    async def display_resume(self, message):
        await message.reply('***Music playback resumed.***')

    @commands.command(name='pause', help='Pause the music playback.')
    async def pause_command(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            self.is_paused = True
            await self.display_pause(ctx.message)

    async def on_message(self, message):
        if self.pause_command_pattern.search(message.content):
            await self.display_pause(message)

    async def display_pause(self, message):
        await message.reply('***Music playback paused.***')

    @commands.command(name='play', help='Play a song.')
    async def play_command(self, ctx, url):
        if not (url.startswith("https://www.youtube.com/watch?v=") | url.startswith("https://youtu.be/")):
            await ctx.send("Please provide a valid HTTPS Youtube URL.")
            return
        else:
            await self.display_play(ctx.message)
        await self.display_play2(ctx.message)
        await self.play(ctx, url)

    async def on_message(self, message):
        if self.play_command_pattern.search(message.content):
            await self.display_play(message)

    async def on_message(self, message):
        if self.play_command_pattern2.search(message.content):
            await self.display_play2(message)

    async def display_play(self, message):
        await message.reply('***Adding song to queue, Please wait...***\n***You can input others command after a song is played.***')

    async def display_play2(self, message):
        await message.reply('***Added to queue successful!***')

    @commands.command(name='next', help='Play the next song.')
    async def next_command(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('***Searching for the next song...***')

    @commands.command(name='queue', help='Show the current queue.')
    async def show_queue(self, ctx):
        await self.display_queue(ctx.message)

    async def display_queue(self, message):
        if not self.queue:
            await message.reply("***The queue is empty.***")
        else:
            tasks = [self.get_filename(index, entry) for index, entry in enumerate(self.queue)]
            filenames = await asyncio.gather(*tasks)

            response_message = 'Next Songs in the queue:'
            for index, filename in enumerate(filenames):
                filename = filename.split('[')[0].strip()  # Remove brackets and extra spaces
                response_message += f'\n{index + 1}. {filename}'

            await message.reply(response_message)

    async def on_message(self, message):
        if self.show_queue_command_pattern.search(message.content):
            await self.display_queue(message)

    async def get_filename(self, index, entry):
        filename, _ = await YTDLSource.from_url(entry[0], loop=self.bot.loop)
        return filename


async def setup(bot):
    await bot.add_cog(Music(bot))