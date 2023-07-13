import requests
import discord
import os
from get_torrent import search, clean_links,grab_torrent, fetch_hash
from discord.ext import commands
import pprint
import json


intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)

token = os.environ.get('DISCORD_TOKEN_KRAKED')
query=''

@bot.event
async def on_ready():
    activity = discord.Game(name="/helpme", type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)
    print('Kraked is lurking for cracks, wtf?')

#this mehthods needs an API but the issue is that it only get the SCENE releases 
#def send_req(search_query):
#   search_query = search_query.replace(' ','.')
#   url =f'https://api.srrdb.com/v1/search/{search_query}/category:pc'
#   response = requests.get(url)
#   if response.status_code == 200:
#       output = ''
#       data = response.json()
#       #check if a release is cracked or not
#       if data["resultsCount"]>=1:
#           global is_cracked
#           is_cracked = True
#       elif data["resultsCount"]==0:
#           
#           is_cracked = False
#       for releases in data["results"]:
#           output = output+releases["release"]+'\n'
#       return output
#   else:
#       print(f'Error {response.status_code}')

@bot.command()
async def status(message, *args):
    query = '.'.join(args)
    result = search(query)
    text = ''
    for key,value in result.items():
        text += clean_links(key).replace('-',' ') +' | ' + value +'\n'

    if len(result)>0:
        title = "Status: Cracked ✅ \nReleases:"
        color =0x00ff00
        embed = discord.Embed(title=title, description = text , color=color)
    else:
        title ="Status : Not Cracked! 😔"
        color=0xff0000
        embed = discord.Embed(title=title, description = '' , color=color)
    await message.send(embed=embed)

@bot.command()
async def helpme(message):
    description = 'Kraked is a simple discord bot that checks if a game has been cracked or not.\n\nCommands:\n\n\n status:\n\n /status <name of a game> \n\nversion = 1.0'
    embed = discord.Embed(title='Commands', description=description,color=0x00ff00)
    await message.send(embed=embed)


@bot.command()
async def grabnfo(message, *args):
    url=f'https://api.srrdb.com/v1/nfo/{args[0]}'
    response = requests.get(url=url)
    data = response.json()
    if response.status_code == 200:
        #embed = discord.Embed(title='NFO', description=data['nfolink'],color=0x00ff00)
        await message.reply(f'Request for: nfo {args[0]} \n {data["nfolink"]}')
    else:
        print(response.status_code)


    


bot.run('MTEyMDM0NjcyMzY2ODIwNTU4OA.G1DZJg.TmWMh3Dp9CmQZ81Gfb2xnPo_cqIZEDQfobtGCg')
