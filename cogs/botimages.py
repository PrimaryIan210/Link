import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
import random
import os
from conf import conf

from permissions import command

# Hi

class BotImages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("BotImages cog started")

    #-----------Change Avatar--------#
    @command(help="Changes the bots avatar to a random image in the directory.", grant_level="explicit")
    async def randompfp(self, ctx, *, spec_bot : str):
        Link_pfp = []
        for filename in os.listdir(conf.pfpDir):
            Link_pfp.append(os.path.join(conf.pfpDir, filename))
        avatars = random.choice(Link_pfp)
        with open(avatars, "rb") as f:
            await self.bot.user.edit(avatar=f.read())

    #-------Profile image uploader------#
    @command(help="Uploads an image to the bot's directory and changes the profile to said image.", grant_level="explicit")
    async def setprofile(self, ctx):
        if len(ctx.message.attachments) == 1:
            attachment = ctx.message.attachments[0]
        elif len(ctx.message.attachments) == 0:
            messages = []
            async for message in ctx.channel.history(limit=2):
                messages.append(message)
            message = messages[-1]
            try:
                attachment = message.attachments[-1]
            except IndexError:
                await ctx.send("You did not attach a file for analysis. You must either do so, or the previous post must contain an attached file.")
                return False
        else:
            await ctx.send("I can only check one image at a time.")
            return False
        original_name, extension = os.path.splitext(attachment.filename)
        file_handle = open(os.path.join(conf.pfpDir, str(attachment.id) + extension), "wb")
        await attachment.save(file_handle)
        file_handle.close()
        with open(os.path.join(conf.pfpDir, str(attachment.id) + extension), "rb") as f:
            await self.bot.user.edit(avatar=f.read())

    #----------Add image------------#
    @command(help="Adds image to bot's directory.", grant_level="explicit")
    async def imageadd(self, ctx):
        if len(ctx.message.attachments) == 1:
            attachment = ctx.message.attachments[0]
        elif len(ctx.message.attachments) == 0:
            messages = []
            async for message in ctx.channel.history(limit=2):
                messages.append(message)
            message = messages[-1]
            try:
                attachment = message.attachments[-1]
            except IndexError:
                await ctx.send("You did not attach a file for analysis. You must either do so, or the previous post must contain an attached file.")
                return False
        else:
            await ctx.send("I can only check one image at a time.")
            return False
        original_name, extension = os.path.splitext(attachment.filename)
        file_handle = open(os.path.join(conf.pfpDir, str(attachment.id) + extension), "wb")
        await attachment.save(file_handle)
        file_handle.close()

    #-------Specified Avatar Change-----#
    @command(help="Changes bot's profile to a specified image in the directory.", grant_level="explicit")
    async def setpfp(self, ctx, picture : str):
        try:
            with open(os.path.join(conf.pfpDir, picture), "rb") as f:
                await self.bot.user.edit(avatar=f.read())
                await ctx.send("Profile image changed to `" + picture + "`")

        except FileNotFoundError:
            await ctx.send("That file doesn't exist")

def setup(bot):
    bot.add_cog(BotImages(bot))
