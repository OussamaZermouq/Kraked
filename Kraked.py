import requests
import discord
import os
from discord.ext import commands


intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)

token = os.environ.get('DISCORD_token_KRAKED')
query=''



@bot.event
async def on_ready():
    activity = discord.Game(name="/helpme", type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)
    print('Kraked is lurking for cracks, wtf?')


def send_req(search_query):
    search_query = search_query.replace(' ','.')
    url =f'https://api.srrdb.com/v1/search/{search_query}/category:pc'
    response = requests.get(url)
    if response.status_code == 200:
        output = ''
        data = response.json()
        #check if a release is cracked or not
        if data["resultsCount"]>=1:
            global is_cracked
            is_cracked = True
        elif data["resultsCount"]==0:
            
            is_cracked = False
        for releases in data["results"]:
            output = output+releases["release"]+'\n'
        return output
    else:
        print(f'Error {response.status_code}')


@bot.command()
async def status(message, *args):
    query = '.'.join(args)
    result = send_req(query)
    if is_cracked ==True:
        title = "Status: Cracked ✅ \nReleases:"
        color =0x00ff00
    else:
        title ="Status : Not Cracked! 😔"
        color=0xff0000
    embed = discord.Embed(title=title, description = result , color=color)
    await message.send(embed=embed)


@bot.command()
async def helpme(message):
    description = 'Kraked is a simple discord bot that checks if a game has been cracked or not.\n\nCommands:\n\n\n status:\n\n \status <name of a game> \n\n\n\n version = 1.0'
    embed = discord.Embed(title='Commands', description=description,color=0x00ff00)
    await message.send(embed=embed)

bot.run(token)
