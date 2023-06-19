import requests
import discord
import typing
from discord.ext import commands
from discord import app_commands


intents = discord.Intents.all()

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='/', intents=intents)

TOKEN= 'MTEyMDM0NjcyMzY2ODIwNTU4OA.GCt14g.4ySAAK5s07-PXBu_7PjbqOfc8vzOU6JHAjoKus'



@bot.tree.command()
async def status(interaction:discord.Integration,
                item: str):
    await interaction.response.send_message("status")
    
@status.autocomplete("item")
async def status_autocompletion(
    interaction:discord.Integration,
    current:str
)-> typing.List[app_commands.Choice[str]]:
    data=[]
    for choice in ['Status','Help']:
        data.append(app_commands.Choice(name=choice,value=choice))
        return data
    


'''@bot.command(name="status", description="Check if a game has been cracked")
async def status(ctx: commands.Context):
    await ctx.send('test')
'''

        

def send_req(search_query):
    search_query = search_query.replace(' ','.')
    url =f'https://api.srrdb.com/v1/search/{search_query}/category:pc'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for releases in data["results"]:
            print(releases["release"])
    else:
        print(f'Error {response.status_code}')



bot.run(TOKEN)