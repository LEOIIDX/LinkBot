'''
LinkBot
By: LEO2DX
main.py

Priority TODO

General TODO

Known Bugs
Nothing to report yet yay!

Import List
os: for filesystem interactions
discord: for use of discord objects
random: For randomized elements
re: for text formatting
string: for im message formatting
discord.ext-commands: for command creation
dotenv-load_dotenv: environment variables for Discord Token
leoDictionary: container for classes relating to dictionaries
leoEmbed: container of Discord Embeds
leoFunc: container for functions
'''
import os
import discord
import random
import re
import asyncio
import string
import math
import json
import sys
import datetime
import shutil
import csv
import base64
import leoFunc

from discord.ext import commands
from dotenv import load_dotenv
from leoDictionary import dictionaryStatuses

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

os.system('clear')

#intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.emojis = True
intents.reactions = True

global version
version = os.popen('git rev-parse HEAD').read()
print('LinkBot\n' + 'Commit: ' + str(version))

'''
Debug Mode details
sets various bot behaviors that make it easier to prod for bugs.

debugValue = 0: no debug functionality
debugValue = 1: prints message debug info to console and sets all chances to 100%
debugValue = 2: only prints message debug info

-Changes command prefix to kyt!
'''
masterQuery = 0
#! DEBUG VALUE IS SET BY ".env" FILE (DONE IN ORDER TO DIFFERENTIATE BETWEEN WORKSTATIONS AND THE HOST SERVER)
debugValue = int(os.getenv('DEBUG_VALUE'))

stDict = dictionaryStatuses()

global sPick
sPick = str(random.randint(1, len(stDict.multiStatus)))

'''
command section
command prefix ky!
'''
if debugValue >= 1:
	bot = commands.Bot(command_prefix='lbt!',intents=intents)
else:
	bot = commands.Bot(command_prefix='lb!',intents=intents)

bot.remove_command('help')
'''
Changes the status randomly on startup
Statuses come from dictionary generated from a txt file
'''

memberCounterChannel = 837031791994208258
memberCounterChannelTest = 846244059768029265
qotdCh = 867088318466359338
global responseCheck
responseCheck = 1

@bot.event
async def on_ready():
	sDict = dictionaryStatuses()

	if debugValue > 0:
		print('DEBUG MODE ACTIVE')
		await bot.change_presence(status=discord.Status.online, activity=discord.Game('TWITTER LINK DEBUG'))
	else:
		print('Bot is ready!!\n')
		await bot.change_presence(status=discord.Status.online, activity=discord.Game(sDict.multiStatus.get(sPick)))

#command error handler
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Command missing arguments')

@bot.command(name='restart') #Restarts the bot, simple as - leo
@commands.has_any_role("Admin", "Mod")
async def restart(ctx):
        await ctx.channel.send("Restarting LinkBot")
        os.execv(sys.executable, ['python3'] + sys.argv)

@bot.command(name='gitpull') #Pulls latest commit and prints command output into chat - leo
@commands.has_any_role("Admin", "Mod")
async def gitpull(ctx):
        await ctx.channel.send(os.popen('git pull').read())

'''
Message Handler
Will check if a message only has a twitter/x link and convert it to a fxtwitter/fixvx link.
'''
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	if debugValue >= 1:
		if message.content[0:4] == 'lbt!': ##ignores kyt! commands
			await bot.process_commands(message)
			return
	else:
		if message.content[0:3] == 'lb!': ##ignores ky! commands
			await bot.process_commands(message)
			return

	if debugValue >= 1:
		print('MESSAGE DEBUG VIEW\n')
		print('Message Guild: ' + str(message.guild))
		print('Message Channel: ' + str(message.channel))
		print('Message Author: ' + str(message.author))
		print('Message Content: ' + str(message.content) + '\n')

	if "https://x.com/" in message.content:
		link = str(message.content)
		newLink = link.replace("x.com", "fixvx.com")
		await message.edit(suppress=True)
		await message.channel.send(newLink)
		return
	elif "https://twitter.com/" in message.content:
		link = str(message.content)
		newLink = link.replace("twitter.com", "vxtwitter.com")
		await message.edit(suppress=True)
		await message.channel.send(newLink)
		return
	elif "https://www.pixiv.net/" in message.content:
		link = str(message.content)
		newLink = link.replace("pixiv.net", "phixiv.net")
		await message.edit(suppress=True)
		await message.channel.send(newLink)
		return

	return

bot.run(TOKEN)
