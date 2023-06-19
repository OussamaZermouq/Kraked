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
output='\n'


def send_req(search_query):
    search_query = search_query.replace(' ','.')
    url =f'https://api.srrdb.com/v1/search/{search_query}/category:pc'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()    
        for releases in data["results"]:
            output =+ releases+'\n'
        return output
    else:
        print(f'Error {response.status_code}')


@bot.command()
async def status(message, *args):
    query = '.'.join(args)
    embed = discord.Embed(title="Status", description=send_req(query), color=0x00ff00)
    await message.send(embed=embed)



bot.run(TOKEN)