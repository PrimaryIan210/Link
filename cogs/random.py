from __future__ import print_function
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
import random
import os
from conf import conf
import json
import urllib

from permissions import command

class RandomStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabledUsers=[conf.ownerID]
        print("RandomStuff cog started")
    #---------Doubt----------#
    @command(help="Presses 'X' to doubt.")
    async def x(self, ctx):
        await ctx.message.delete()
        await ctx.send("Press X to doubt...")
        await ctx.channel.send(file=discord.File(os.path.join(conf.imgDir, 'doubt.jpg')))

    #-----------------Tableflip----------#
    @command(help="Flips the table for Mobile users.")
    async def tableflip(self, ctx):
        await ctx.message.delete()
        await ctx.send('(╯°□°）╯︵ ┻━┻')

    #-------------Spilled milk----------------#
    @command(help="Only those worthy enough can use this.", grant_level="explicit")
    async def spiltmilk(self,ctx):

        milk = []

        for filename in os.listdir(conf.imgDir + "Milk/"):
            milk.append(os.path.join(conf.imgDir + "/Milk/", filename))
        choice = random.choice(milk)
        await ctx.channel.send(file=discord.File(choice))

    #-------------------Depression------------#
    @command(help="When you're depressed.")
    async def depression(self, ctx):
        await ctx.message.delete()

        depression = []

        for filename in os.listdir(conf.imgDir + "Depression/"):
            depression.append(os.path.join(conf.imgDir + "/Depression/", filename))
        choice = random.choice(depression)
        await ctx.channel.send(file=discord.File(choice))

    #-----------Ping-----------#
    @command(help="Makes sure the bot is responding to the API.")
    async def ping(self, ctx):
        await ctx.send("It's safe to assume that I'm fine.")

    # #-----------Blackjack dealer-------------#
    # @commands.command(help="Emulates a Blackjack dealer.")
    # async def blackjack(self, ctx):
    #     QUARTER_DECK = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    #
    #     hand= []
    #
    #     hand.append(random.choice(QUARTER_DECK))
    #     hand.append(random.choice(QUARTER_DECK))
    #
    #     while True:
    #         if sum(hand) < 17:
    #             await ctx.send("Hitting with: " + str(sum(hand)))
    #             new_card = random.choice(QUARTER_DECK)
    #             if new_card == 11 and sum(hand) + 11 > 21:
    #                 new_card = 1
    #             hand.append(new_card)
    #             await ctx.send("Dealer got: " + str(new_card))
    #         elif sum(hand) >= 17 and sum(hand) <= 21:
    #             if sum(hand) == 21 and len(hand) == 2:
    #                 await ctx.send("BLACKJACK!")
    #                 break
    #             else:
    #                 await ctx.send("Staying with: " + str(sum(hand)))
    #                 break
    #         else:
    #             if sum(hand) > 21:
    #                 await ctx.send("BUST with: " + str(sum(hand)))
    #                 break
    #         await asyncio.sleep(1)

    # @commands.command()
    # async def randomhydrate(self, ctx):
    #     if ctx.message.channel.id == 751133278710398986:
    #         role = discord.utils.get(ctx.guild.roles, name="Gaggle Gang")
    #         random_member = random.choice(role.members)
    #         await ctx.send(random_member.mention + "You have been randomly selected to hydrate! Consider yourself (and your liver) lucky!")
    #     else:
    #         await ctx.send("This command was not designed for this channel.")

def setup(bot):
    bot.add_cog(RandomStuff(bot))
