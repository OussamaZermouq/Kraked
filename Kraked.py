import requests
import discord
import os
from get_torrent import clean_links, grab_torrent, fetch_url
from get_cracks_bitsearch import search
from get_cracks_onlinefix import search_online, get_torrent_file
from discord.ext import commands
import urllib
from art import text2art
import sys
from dotenv import load_dotenv
from discord.ui import Select, View

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)
load_dotenv()
token = os.getenv("BOT_TOKEN")


@bot.event
async def on_ready():
    activity = discord.Game(name="/helpme", type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)
    await bot.tree.sync()
    print("Kraked is lurking for cracks, wtf?")
    print(text2art("KRAKED", font="rand"))


# this mehthods needs an API but the issue is that it only get the SCENE releases not the p2p ones
# def send_req(search_query):
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
#           is_cracked = False
#       for releases in data["results"]:
#           output = output+releases["release"]+'\n'
#       return output
#   else:
#       print(f'Error {response.status_code}')


@bot.tree.command(name="status", description="Search for a game if its cracked or not.")
async def slash_command(interaction: discord.Interaction, game_name: str):
    print(f"looking for {game_name}")
    text = ""
    link = "Link"
    result = search(game_name)
    for release in result:
        hyperlink = f'[{link}]({release[3].replace(" ","%20")})'  # -_-
        text += (
            release[0]
            + " | "
            + release[1]
            + " | "
            + release[2]
            + " Seeders |"
            + hyperlink
            + "\n"
        )

    if len(result) > 0:
        if sys.getsizeof(text) > 4000:
            text = "I have found too many releases please be more specific."
        title = "Status: Cracked ✅ \nReleases:"
        color = 0x00FF00
        embed = discord.Embed(title=title, description=text, color=color)
        if interaction.user.avatar is None:
            embed.set_footer(text=f"Request made by @{interaction.user.name}")
        else:
            embed.set_footer(
                text=f"Request made by @{interaction.user.name}",
                icon_url=f"{interaction.user.avatar.url}",
            )

    else:
        title = "Status : Not Cracked! 😔"
        color = 0xFF0000
        embed = discord.Embed(
            title=title, description="Nothing to see here", color=color
        )
        if interaction.user.avatar is None:
            embed.set_footer(text=f"Request made by @{interaction.user.name}")
        else:
            embed.set_footer(
                text=f"Request made by @{interaction.user.name}",
                icon_url=f"{interaction.user.avatar.url}",
            )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="helpme", description="Get help")
async def slash_command(interaction: discord.Interaction):
    help_embed = discord.Embed(
        title="Commands", description="List of all commands", color=0x00FF00
    )
    help_embed.set_author(name="Kraked", icon_url=None)
    help_embed.add_field(
        name="description",
        value="Kraked is a simple discord bot that checks if a game has been cracked or not.",
        inline=False,
    )
    help_embed.add_field(
        name="/status <name of a game>",
        value="Get the status of a game as well as the download links  ",
        inline=False,
    )
    help_embed.add_field(
        name="/grabnfo",
        value="Get the nfo of a scene release (needs the correct scene release title e.g ELDEN.RING.Shadow.of.the.Erdtree-RUNE)",
        inline=False,
    )
    help_embed.add_field(
        name="/status_online <name of a game>",
        value="Get the status of a game in online mode as well as the torrent download link",
        inline=False,
    )

    help_embed.set_footer(text="Version -_- 2.0.1")
    await interaction.response.send_message(embed=help_embed)


@bot.tree.command(name="grabnfo", description="Search for a release's NFO")
async def slash_command(interaction: discord.Interaction, release_name: str):
    url = f"https://api.srrdb.com/v1/nfo/{release_name}"
    response = requests.get(url=url)
    data = response.json()
    if response.status_code == 200:
        embed = discord.Embed(
            title=f"NFO Request for: {release_name} )",
            description=data["nfolink"],
            color=0x00FF00,
        )
        await interaction.response.send_message(embed=embed)

    else:
        await interaction.response.send_message(
            f"Request for: nfo {release_name} \n Not found"
        )


@bot.tree.command(name="status_online", description="Look for online cracks for a game")
async def slash_command(interaction: discord.Integration, game_name: str):
    print(f"looking for {game_name}")
    text = ""
    link = "Link"
    result = search_online(game_name)
    torrents = []
    i = 0
    for release in result:
        # a simple counter to avoid label duplication issue, since it needs to be unique.
        i += 1
        hyperlink = f"[{link}]({release[1]})"  # -_-
        text += f"{release[0]} | {hyperlink}\n"
        torrents.append(discord.SelectOption(
                label=f"{i} • {release[0]}",
                description=f"{release[0]}",
                value=f"{release[1]}",
                )
            )


    select = Select(options=torrents, placeholder="Choose a release for the torrent")
    menu_view = View()
    menu_view.add_item(select)

    async def select_callback(interaction):
        selected_option = interaction.data["values"]
        torrent_name = get_torrent_file(url=selected_option[0])
        await interaction.response.send_message(
            file=discord.File(f'Torrents/{torrent_name}'),
            content = f"You can download the torrent from here!", 
            ephemeral=True
        )
    select.callback = select_callback
        
    if len(result) > 0:
        if sys.getsizeof(text) > 4000:
            text = "I have found too many releases please be more specific."
        title = "Status: Cracked Online ✅ \nReleases:"
        color = 0x00FF00
        embed = discord.Embed(title=title, description=text, color=color)
        if interaction.user.avatar is None:
            embed.set_footer(text=f"Request made by @{interaction.user.name}")
        else:
            embed.set_footer(
                text=f"Request made by @{interaction.user.name}",
                icon_url=f"{interaction.user.avatar.url}",
            )

    else:
        title = "Status : Online Not Cracked! 😔"
        color = 0xFF0000
        embed = discord.Embed(
            title=title,
            description="Nothing to see here try /status maybe ¯\_(ツ)_/¯",
            color=color,
        )
        if interaction.user.avatar is None:
            embed.set_footer(text=f"Request made by @{interaction.user.name}")
        else:
            embed.set_footer(
                text=f"Request made by @{interaction.user.name}",
                icon_url=f"{interaction.user.avatar.url}",
            )
    await interaction.response.defer()
    await interaction.followup.send(embed=embed, view=menu_view)


bot.run(token)
