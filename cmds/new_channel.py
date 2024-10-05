# new_channel.py
from discord.ext import commands
import discord

@commands.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='nonamed-channel'):
    guild = ctx.guild

    # Ensure the name is valid for a channel
    channel_name = channel_name.replace(' ', '-')  # Replace spaces with hyphens
    channel_name = discord.utils.escape_markdown(channel_name)  # Escape any markdown characters
    channel_name = channel_name[:100]  # Limit the length to 100 characters

    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    
    if existing_channel:
        await ctx.send(f'Error: Channel "{channel_name}" already exists.')
    elif any(char.isdigit() for char in channel_name):
        await ctx.send('Error: Channel names cannot contain numbers.')
    else:
        try:
            print(f'Creating a new channel: {channel_name}')
            new_channel = await guild.create_text_channel(channel_name)

            # Move the new channel to the last position
            position = len(guild.channels)
            await new_channel.edit(position=position)

            await ctx.send(f'Channel "{new_channel.name}" created successfully!')
        except discord.Forbidden:
            await ctx.send('Error: The bot does not have permission to create channels.')
        except discord.HTTPException as e:
            await ctx.send(f'Error: Failed to create channel. Reason: {e}')

def setup(bot):
    bot.add_command(create_channel)
