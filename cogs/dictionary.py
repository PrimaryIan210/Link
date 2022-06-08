import asyncio
import discord
from discord.ext import commands
from wordster import wordster
import urbandict
import Linkconfig

class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Expiremental Dictionary cog started")
    @commands.command(pass_context=True, no_pm=True, help="Currently doesn't work. Gets the definition of a word from Merriam-Webster.")
    async def define(self, ctx, *, word : str):
        wordDef = wordster.find_meaning(str(word))
        await ctx.send(str(wordDef))

    @commands.command(pass_context=True, no_pm=True, help="Beta. Gets the definition of a word from Urban Dictionary.")
    async def urban(self, ctx, *, word : str):
        wordDef = urbandict.define(word)
        await ctx.send(str(wordDef))
