from discord.ext import commands
from basketball_reference_scraper.teams import get_roster
from basketball_reference_scraper.seasons import get_standings, get_schedule
from basketball_reference_scraper.box_scores import get_box_scores
from basketball_reference_scraper.players import get_stats
from datetime import date
from bs4 import BeautifulSoup
from prsaw import RandomStuff
import random
import discord
import requests
import pandas as pd


bot = commands.Bot(command_prefix = '!')
rs = RandomStuff(async_mode=True)

#ai chat
@bot.event
async def on_message(message):
    if bot.user == message.author:
        return

    if message.channel.id == 849438653079224392:
        if message.content[0] != '!':
            response = await rs.get_ai_response(message.content)
            await message.reply(response)  
    
    await bot.process_commands(message)
    
    

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    bot.run(TOKEN)

