import asyncio
import discord
from discord.ext import commands
import random
import os
import pickle
from conf import conf
from permissions import command

class FinalFantasy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Final Fantasy XIV cog started")

    @command(help="Generates Jumbo Cactpot lottery numbers")
    async def cactpot(self, ctx, *, amount : int=None):
        num = random.randint(0, 9999)
        nums = [n for n in str(num)]
        nums = "0 " * (4 - len(nums)) + " ".join(nums)
        return await ctx.send("Random numbers: " + nums)

def setup(bot):
    bot.add_cog(FinalFantasy(bot))
