import requests
import discord
import typing
from discord.ext import commands
from discord import app_commands


intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)
TOKEN= 'MTEyMDM0NjcyMzY2ODIwNTU4OA.GCt14g.4ySAAK5s07-PXBu_7PjbqOfc8vzOU6JHAjoKus'
query=''

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
        title = "Stauts: Cracked ✅ \nReleases:"
        color =0x00ff00
    else:
        title ="Status : Not Cracked! 😔"
        color=0xff0000
    embed = discord.Embed(title=title, description = result , color=color)
    await message.send(embed=embed)



bot.run(TOKEN)