from __future__ import print_function
import asyncio
import discord
from discord.ext import commands, tasks
from discord.ext.commands.errors import MissingRequiredArgument
import os
import sys
import traceback
import datetime
import random
from conf import conf
import pickle

from aiohttp.web import AppRunner, TCPSite

import pidfile

from cogs.profile import Profile
from cogs.games import Games
from cogs.admin import Admin
from cogs.random import RandomStuff
from cogs.botimages import BotImages
# from cogs.cog_dictionary import Dictionary
#from cogs.cog_pokedex import Pokedex
#from cogs.cog_rpg import RPG
from cogs.audio import Audio
#from cogs.dash.dash import Dash
from cogs.finalFantasy import FinalFantasy
from ext.help import log

log("Initializing Bot")


bot = commands.Bot (command_prefix=commands.when_mentioned_or(conf.prefix), description=conf.description)
extensions = [
    'cogs.admin',
    'cogs.botimages',
    'cogs.games',
    #'cogs.cog_pokedex',
    'cogs.profile',
    'cogs.random',
    'cogs.audio',
    #'cogs.cog_rpg'
    'cogs.finalFantasy'
]

for extension in extensions:
    try:
        bot.load_extension(extension)
    except Exception:
        print("Failed to load extension {extension}.".format(extension=extension))
        traceback.print_exc()

@bot.event
async def on_ready():
    #os.system("clear")
    log('A Hero is Born as:\n{0}  (ID: {0.id})'.format (bot.user))

    # bot.dash = Dash(bot)
    # await bot.dash.setup()
    # bot.dash_runner = AppRunner(bot.dash.app)
    # await bot.dash_runner.setup()
    # bot.site = TCPSite(bot.dash_runner, 'localhost', 8080)
    # await bot.site.start()

    try:
        game = pickle.load(open("game.pickle", "rb"))
        activity = pickle.load(open("activity.pickle", "rb"))
        if activity == "active":
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=str(game.replace("_", " ")) + " | Use $help"))
        if activity == "dnd":
            await bot.change_presence(status=discord.Status.online.dnd, activity=discord.Game(name=str(game.replace("_", " ")) + " | Inactive"))
        if activity == "streaming":
            await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name=str(game.replace("_", " ")), url = "https://twitch.tv/primaryian210") + " | Use $help")
    except FileNotFoundError:
        pass

    try:
        channel = pickle.load(open("channel.pickle", "rb"))
        channelLoc = bot.get_channel(channel)
        log("Initialization complete.")
        await channelLoc.send("<@" + str(conf.ownerID) + "> restart complete.")
        os.remove("channel.pickle")
    except FileNotFoundError:
        pass


@bot.event
async def on_message(message):
    if message.author.id != bot.user.id: #Bot's ID to make sure that it doesn't get stuck in a loop
        if message.author == bot.user:
            return
        if message.author.bot: return
        await bot.process_commands(message)
        ctx = await bot.get_context(message)
        # await bot.get_cog("RPG").process(ctx)

@bot.event
async def on_command_error(ctx, error):
    error = getattr(error, "original", error)
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"Missing Permissions: `{ctx.command.node(bot)}`.")
    else:
        raise error


# @bot.event
# async def on_voice_state_update(member, before, after):
#     channel = bot.get_channel(402773748643528704)
#     await channel.send("Test")

if __name__ == '__main__':
    try:
        with pidfile.PIDFile():
            bot.run(conf.token)
    except pidfile.AlreadyRunningError:
        print("UH OH")
        sys.exit(1)
