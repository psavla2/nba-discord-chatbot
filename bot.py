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

# get roster
@bot.command(name = "roster")
async def roster(ctx, team:str, year:int):
    df = get_roster(team, year)
    query = df[['NUMBER', 'PLAYER','POS']].to_string()
    result = "```" + query + "```"
    await ctx.send(result);

# get standings
@bot.command(name = "standings")
async def standing(ctx, conference:str):
    standing = get_standings()
    query = standing[conference][['TEAM', 'W', 'L','GB']].to_string()
    result = "```" + query + "```"
    await ctx.send(result)

#get box-score
@bot.command(name = "box-score")
async def score(ctx, team1:str, team2: str, date: str):
    box_score = get_box_scores(date, team1, team2)
    
    query = box_score[team1][['PLAYER', 'PTS', 'TRB', 'AST', 'STL', 'BLK']].to_string()
    result = "```" + query + "```"
    await ctx.send(result)
    query = box_score[team2][['PLAYER', 'PTS', 'TRB', 'AST', 'STL', 'BLK']].to_string()
    result = "```" + query + "```"
    await ctx.send(result)

#get stats for a player
@bot.command(name = "stat")
async def stat(ctx, first:str, last:str):
    stats = get_stats(first + last, stat_type='PER_GAME', playoffs=False, career=False)
    query = stats[['SEASON', 'PTS', 'TRB', 'AST', 'STL', 'BLK']].to_string()
    result = "```" + query + "```"
    await ctx.send(result)

#scrape statmuse for answer to a question
@bot.command(name = "question")
async def stat(ctx, *arg):
    URL = 'https://www.statmuse.com/ask/nba/'
    for word in arg:
        URL += word + "-" 
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='cover')  
    answer = results[0]
    await ctx.send(answer.p.text)

#get schedule
@bot.command(name = "schedule")
async def stat(ctx, teamf: str, teaml: str, year: int):
    schedule = get_schedule(year, playoffs=False)
    team =  teamf + " " + teaml
    filtered = schedule.loc[(schedule['VISITOR'] == team) | (schedule['HOME'] == team)]
    value_to_check = pd.Timestamp(date.today())
    filtered_date = filtered['DATE'] > value_to_check
    query = filtered[filtered_date].to_string()
    result = "```" + query + "```"
    await ctx.send(result)
    
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

