import discord
from discord.ext import commands
from discord_components import *
from discord import Spotify
import os
import sys

intents = discord.Intents().all()
client = commands.Bot(command_prefix = 'x', intents = intents) 
DiscordComponents(client)


xtoken = open("token.txt")
for numbers in xtoken:
    token = numbers

@client.event
async def on_ready(): #runs when the bot is ready
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the world burn."))
    print(sys.executable)
    print('onobot is up')

@client.command()
async def ping(ctx):
    """Check bot ping"""
    await ctx.send(f'Pong! {round(client.latency *1000)} ms')

@client.command()
async def videos(ctx):
    await ctx.send('https://tenor.com/view/bruh-moment-bruh-moment-recording-gif-14698316')


@client.command()
async def question(ctx):
    await ctx.send(
        "Are you gay?",
        components = [
            Button(label = "YES", custom_id = "button1")
        ],
    )
    while True:
        interaction = await client.wait_for("button_click", check = lambda i: i.custom_id == "button1")
        await interaction.send(content = f"HAHA <@{interaction.user.id}> YOU ARE NOW, THE GAYYYYYYYYYYYYYYYYYYYYYYY!")


@client.command()
async def spotify(ctx,user:discord.Member=None):
    #""" :Displays what song your playing on spotify (supposedly)"""
    #if not user:
        #user = message.author.id
    user = ctx.author
    userid = f'<@{ctx.author.id}>'
    for activity in user.activities:
        if isinstance(activity, Spotify):
            await ctx.send(f"{userid} is listening to {activity.title} by {activity.artist}")
        #else:
            #   await ctx.send(f"{userid}, your're not listening to anything my dude")
                    
    #sname = discord.Spotify.title
    #sartists = discord.Spotify.artists
    #album = discord.Spotify.album
    #palbum = discord.Spotify.album_cover_url
    #duration = discord.Spotify.duration
    #name = sname.fget()
    #message = ctx.send(name)
    #await message
for filename in os.listdir('./cogs'): #loops for all the files and checks if its a py file
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}') #removes the last 3 charactes (also loads the thingy)

client.run(token)