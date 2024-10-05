import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import sys

from listener.new_memberjoin import setup as new_memberjoinsetup
from cmds import updateactivity

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    print('Error: Discord token not found. Make sure you have set the DISCORD_TOKEN environment variable.')
    sys.exit()

intents = discord.Intents.default()
intents.members = True  # Enable the GUILD_MEMBERS intent
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize a dictionary to store roles_message_id for each guild
bot.guild_roles_message_ids = {}

# Function to show and activating the update_activity
async def perform_startup_actions():
    print('Performing startup actions...')
    print('Hello, Welcome!')
    await updateactivity.update_activity(bot)
# The end of function to show and activating the update_activity

# Function that when you start program / running / resumed the program, it will do some function (call function)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # to greet new member in dm and channel
    new_memberjoinsetup(bot)

    # bot for music
    if 'cogs.musicbot' not in bot.extensions:
        try:
            await bot.load_extension('cogs.musicbot')
            print('Successfully loaded extension: cogs.musicbot')
        except Exception as e:
            print(f'Failed to load extension cogs.musicbot: {e}')

    # Import and setup math commands
    if 'cogs.math' not in bot.extensions:
        try:
            await bot.load_extension('cogs.math')
            print('Successfully loaded extension: cogs.math')
        except Exception as e:
            print(f'Failed to load extension cogs.math: {e}')

    # Import and setup chemistry commands
    if 'cogs.chemistry_cog' not in bot.extensions:
        try:
            await bot.load_extension('cogs.chemistry_cog')
            print('Successfully loaded extension: cogs.chemistry_cog')
        except Exception as e:
            print(f'Failed to load extension cogs.chemistry_cog: {e}')
    
    # Import command for report general
    if 'cogs.report' not in bot.extensions:
        try:
            await bot.load_extension('cogs.report')
            print('Successfully loaded extension: cogs.report')
        except Exception as e:
            print(f'Failed to load extension cogs.report: {e}')

    # Import bot cuaca
    if 'cogs.bot_cuaca' not in bot.extensions:
        try:
            await bot.load_extension('cogs.bot_cuaca')
            print('Successfully loaded extension: cogs.bot_cuaca')
        except Exception as e:
            print(f'Failed to load extension cogs.report: {e}')
            
    # Import bot youtube notif
    if 'listener.YoutubeNotifBot' not in bot.extensions:
        try:
            await bot.load_extension('listener.YoutubeNotifBot')
            print('Successfully loaded extension: listener.YoutubeNotifBot')
        except Exception as e:
            print(f'Failed to load extension listener.YoutubeNotifBot: {e}')

    # if 'cogs.bot_adzan' not in bot.extensions:
    #     try:
    #         await bot.load_extension('cogs.bot_adzan')
    #         print('Successfully loaded extension: cogs.bot_adzan')
    #     except Exception as e:
    #         print(f'Failed to load extension cogs.bot_adzan: {e}')

    if 'cogs.cs2_status' not in bot.extensions:
        try:
            await bot.load_extension('cogs.cs2_status')
            print('Successfully loaded extension: cogs.cs2_status')
        except Exception as e:
            print(f'Failed to load extension: cogs.cs2_status: {e}')

    if 'cogs.faceit_cs2_status' not in bot.extensions:
        try:
            await bot.load_extension('cogs.faceit_cs2_status')
            print('Successfully loaded extension: cogs.faceit_cs2_status')
        except Exception as e:
            print(f'Failed to load extension: cogs.faceit_cs2_status: {e}')

    # Run perform_startup_actions function
    await bot.tree.sync()
    await perform_startup_actions()
# The end of function that when you start program / running / resumed the program, it will do some function (call function)

# Function that show your program is connected to discord
@bot.event
async def on_connect():
    print('Connected to Discord.')
# The end of function that show your program is connected to discord

# Function that show your program is disconnected and reconnecting
@bot.event
async def on_disconnect():
    print('Disconnected from Discord. Reconnecting...')
# The end of function that show your program is disconnected and reconnecting

# Function that show your program is resumed
@bot.event
async def on_resumed():
    print('Resumed session. I\'m back!')
    await perform_startup_actions()
# The end of function that show your program is resumed

# Function to connect / run the discord bot
async def connect():
    while not bot.is_closed():
        try:
            await bot.start(TOKEN, reconnect=True)
        except discord.errors.LoginFailure:
            print('Invalid token. Please check your token.')
            break
        except Exception as e:
            print(f'An error occurred: {e}')
            await asyncio.sleep(5)  # Wait for a few seconds before attempting to reconnect
# End of function connect

# Remove help (!help) base command
bot.remove_command('help')

# Adding new !help command, you can use /help or !help
@bot.hybrid_command()
async def help(ctx):
    embed = discord.Embed(
        title='Shiroz Bot Help',
        description='Hello! This discord bot have feature:\n1. Music \n2. Calculator \n3. Chemistry \n4. Weather \n5. CS2 Profile Checker \n\nHelp command for my bot :',
        color=discord.Color.blue()
    )
    embed.add_field(name='**General Commands: **', value='***!help*** - Show this help message', inline=False)
    embed.add_field(name='**Music Commands Help: **', value='to know how to use music command use ***!help_music*** or ***/help_music***', inline=False)
    embed.add_field(name='**Calculator Commands: **', value='to know how to use calculator command use ***!help_calculator*** or ***/help_calculator***', inline=False)
    embed.add_field(name='**Chemistry Commands: **', value='to know how to use chemistry command use ***!help_chemistry*** or ***/help_chemistry***', inline=False)
    embed.add_field(name='**Weather Commands: **', value='to know how to use weather command use ***!help_weather*** or ***/help_weather***', inline=False)
    embed.add_field(name='**CS2 Profile Checker Commands: **', value='to use CS2 Profile Checker use command ***!cs2info (input url)*** or ***/cs2info !cs2info (input url)***', inline=False)
    # Add more fields for other commands as needed

    await ctx.send(embed=embed)
# The end of !help or /help command code.

# Adding !help_music or /help_music
@bot.hybrid_command()
async def help_music(ctx):
    embed = discord.Embed(
        title='Shiroz Bot Help Music',
        description='Help command using music command :',
        color=discord.Color.blue()
    )
    embed.add_field(name='**Music Commands: **', value='***!play*** - Play a song or add it to next song in queue.\n***example: !play [youtube_url]***\n***!next*** - Next / skip the current song.\n***!queue*** - Show music in queue list.\n***!pause*** - Pause current song.\n***!resume*** - Resume the current song.', inline=False)
    # Add more fields for other commands as needed
    await ctx.send(embed=embed)
# The end of !help_music or /help_music

# Adding !help_calculator or /help_calculator
@bot.hybrid_command()
async def help_calculator(ctx):
    embed = discord.Embed(
        title='Shiroz Bot Help Calculator',
        description='Help command for using calculator command :',
        color=discord.Color.blue()
    )
    embed.add_field(name='**Calculator Commands: **', value='***!math calc*** - Calculator / Evaluate a mathematical expression. add, subtract, multiplication, and division only.\n***example:*** !math calc 10*2-50+10. \n****!math add**** - add n int inputs. \n****example:**** !math add 1 5 \n****!math subtract**** - subtract n int inputs.\n ****example:**** !math subtract 7 5\n****!math multiplication**** - multiplication n int inputs. \n****example:**** !math multiplication 2 5\n****!math division**** - division n int inputs.\n ****example:**** !math divison 10 5', inline=False)
    # Add more fields for other commands as needed
    await ctx.send(embed=embed)
# The end of !help_calculator or /help_calculator

# Adding !help_chemistry or /help_chemistry
@bot.hybrid_command()
async def help_chemistry(ctx):
    embed = discord.Embed(
        title='Shiroz Bot Help Chemistry',
        description='Help command for using chemistry command :',
        color=discord.Color.blue()
    )
    embed.add_field(name='**Chemistry Commands: **', value='***!reaksi-Asam_Basa*** - Search for the results of combining reactions between acids and bases\n***example: !reaksi-Asam_Basa [asam] [basa] -> !reaksi-Asam_Basa HCl NaOH***\n***!report_Chemistry*** - Report for commands in category Chemistry Commands.\n***example: !report_Chemistry no combine result from acids A and bases B***', inline=False)
    # Add more fields for other commands as needed
    await ctx.send(embed=embed)
# The end of !help_chemistry or /help_chemistry
    
# Adding !help_weather or /help_weather
@bot.hybrid_command()
async def help_weather(ctx):
    embed = discord.Embed(
        title='Shiroz Bot Help Weather',
        description='Help command for using weather command :',
        color=discord.Color.blue()
    )
    embed.add_field(name='**Weather Commands: **', value='***!cuaca*** - to show weather in inputed city \n***example: !cuaca Bandung or !cuaca London***', inline=False)
    # Add more fields for other commands as needed
    await ctx.send(embed=embed)
# The end of !help_weather or /help_weather

# COMMAND FOR SEND ROLES (SELECT ROLES BY USER CLICK EMOJI) #
@bot.command()
# Function to send roles to a channel select roles
async def send_roles(ctx):
    roles_message = await ctx.send("Select roles:\n:male_sign:  - ♂ Male Adventure Player\n:female_sign: - ♀ Female Adventure Player\n<:cs2:1188194696133099651> - CS2 Player\n<:valorant:1188189833005367319> - Valorant Player")

    roles_emojis = ['♂️', '♀️', '<:cs2:1188194696133099651>', '<:valorant:1188189833005367319>']  # Emojis corresponding to the roles
    for emoji in roles_emojis:
        await roles_message.add_reaction(emoji)

    # Store the message ID in the guild_roles_message_ids dictionary
    bot.guild_roles_message_ids[ctx.guild.id] = roles_message.id
    print(f"Stored roles_message_id for guild {ctx.guild.id}: {roles_message.id}")
# The end of function to send roles to a channel select roles

# Function that user can react emoji and adding the roles
@bot.event
async def on_reaction_add(reaction, user):
    channel_id = 865958511716204555  # Replace with your channel ID

    # Retrieve roles_message_id from the guild_roles_message_ids dictionary
    roles_message_id = bot.guild_roles_message_ids.get(reaction.message.guild.id)

    if roles_message_id and reaction.message.channel.id == channel_id and reaction.message.id == roles_message_id:
        guild = reaction.message.guild
        member = guild.get_member(user.id)

        roles_mapping = {
            '♂️': ['♂ Male Adventure Player', 'GAMER'],  # Map emoji to role name
            '♀️': ['♀ Female Adventure Player' , 'GAMER'],
            '<:cs2:1188194696133099651>' : ['CS2 Player'],
            '<:valorant:1188189833005367319>' : ['Valorant Player']
        }

        selected_roles = roles_mapping.get(str(reaction.emoji))
        roles = [discord.utils.get(guild.roles, name=role) for role in selected_roles]

        if all(roles) and member:
            await member.add_roles(*roles)
            print(f'Added roles {", ".join(role.name for role in roles)} to {member.display_name}')
# The end of function that user can react emoji and adding the roles

# Function that user can react emoji and delete user own roles
@bot.event
async def on_reaction_remove(reaction, user):
    channel_id = 865958511716204555  # Replace with your channel ID

    # Retrieve roles_message_id from the guild_roles_message_ids dictionary
    roles_message_id = bot.guild_roles_message_ids.get(reaction.message.guild.id)

    if roles_message_id and reaction.message.channel.id == channel_id and reaction.message.id == roles_message_id:
        guild = reaction.message.guild
        member = guild.get_member(user.id)

        roles_mapping = {
            '♂️': ['♂ Male Adventure Player', 'GAMER'],  # Map emoji to role name
            '♀️': ['♀ Female Adventure Player' , 'GAMER'],
            '<:cs2:1188194696133099651>' : ['CS2 Player'],
            '<:valorant:1188189833005367319>' : ['Valorant Player']
        }

        selected_roles = roles_mapping.get(str(reaction.emoji))
        roles = [discord.utils.get(guild.roles, name=role) for role in selected_roles]

        if all(roles) and member:
            await member.remove_roles(*roles)
            print(f'Removed roles {", ".join(role.name for role in roles)} from {member.display_name}')
#The end of function that user can react emoji and delete user own roles
# THE END OF COMMAND FOR SEND ROLES (SELECT ROLES BY USER CLICK EMOJI) #

bot.run(TOKEN)