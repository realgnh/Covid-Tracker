import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from lxml import html

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.activity.Game(name="/help"))
    print(f"{bot.user.name} is ONLINE")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    
    
@bot.tree.command(name="help", description="help of bot")
async def help(interaction: discord.Interaction):
    embed = embed = discord.Embed(title="Help", color=discord.Color.red(), description='do /track to get latest cases, deaths, and recoveries!')
    await interaction.response.send_message(embed=embed)
    

    
@bot.tree.command(name='track', description='sends cases, deaths, and revoveries')
async def track(interaction: discord.Interaction):
    url = 'https://www.worldometers.info/coronavirus/'
    r = requests.get(url)
    
    if r.status_code == 200:
        scrape = html.fromstring(r.content, 'lxml')
        
        path = '/html/body/div[2]/div[2]/div[1]/div/div[4]/div'
        getpath = scrape.xpath(path)
        
        embed = discord.Embed(title="Covid Info", color=discord.Color.dark_red())
        
        for i in getpath:
            embed.add_field(name="Cases:", value=i.text_content().strip(), inline=False)
            
        ndpath = '/html/body/div[2]/div[2]/div[1]/div/div[6]/div'
        getndpath = scrape.xpath(ndpath)
        
        for k in getndpath:
            embed.add_field(name="Deaths:", value=k.text_content().strip(), inline=False)
            
    else:
        print(f'ERROR: {r.status_code} ⚠️')
        
bot.run("MTE5ODAzODE0NDUwNzk3MzcwMg.GcBj9L.cYHhz4q2K8_dyAedzXTOnI6P6NLx9G-0eE4AgA")