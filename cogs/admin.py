from __future__ import print_function
import asyncio
import discord
from discord.ext import commands, tasks
from discord.ext.commands.errors import MissingRequiredArgument

from permissions import command, permission_exists

import os
import psutil
import pickle
from conf import conf
import time
import sys

from cogs.orm.models import Profiles

import random
import json
import urllib
import re
import pyfiglet

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Admin cog started")

    #----------------Restart Link------------------#
    @command(help="Restarts the bot.", grant_level="explicit")
    async def restart(self, ctx, module="bot"):
        if module == "bot":
            async with ctx.typing():
                await ctx.send("Restarting now.")
                pickle.dump(ctx.channel.id, open("channel.pickle", "wb"))
                await self.bot.logout()
                await self.bot.close()
        else:
            for mod in self.bot.extensions:
                if module == mod.split(".")[-1]:
                    self.bot.reload_extension(mod)
                    return await ctx.send("`{cog}` reloaded.".format(cog=mod.split(".")[-1]))
            else:
                return await ctx.send("No cog named `{cog}` exists.".format(cog=mod.split(".")[-1]))


    # #---------Autonomy--------------------#
    # @commands.command(help="Allows for the bot to used for sending messages. Can only be used by Ian, as it is done through the terminal.")
    # async def auto(self, ctx, channel : str):
    #     if ctx.message.author.id == conf.ownerID:
    #         await ctx.message.delete()
    #         while True:
    #             sentMessage = input("What is the message you'd like me to send?")
    #             if sentMessage == "Stop":
    #                 return False
    #             else:
    #                 if channel == "Testing":
    #                     channelLoc = self.bot.get_channel(Linkconfig.testing)
    #                     await channelLoc.send(str(sentMessage))
    #                 elif channel == "Link":
    #                     channelLoc = self.bot.get_channel(Linkconfig.linktest)
    #                     await channelLoc.send(str(sentMessage))
    #                 elif channel == "WSHTF":
    #                     channelLoc = self.bot.get_channel(Linkconfig.wshtf)
    #                     await channelLoc.send(str(sentMessage))
    #                 elif channel == "SSS":
    #                     channelLoc = self.bot.get_channel(751126728402796594)
    #                     await channelLoc.send(str(sentMessage))
    #                 else:
    #                     if channel == "Ygg":
    #                         channelLoc = self.bot.get_channel(294260795465007105)
    #                         await channelLoc.send(str(sentMessage))
    #
    #
    # else:
    #     ctx.send("WOAH! How the fuck did you find that one!")

    #--------Presence changes----------#
    @command(help="Changes the Playing 'Game' status, and presence of the bot.", grant_level="explicit")
    async def activity(self, ctx, spec_bot : str, activities : str, game : str):
        if (spec_bot.lower() == "link") or (spec_bot.lower() == "all"):
            await ctx.message.delete()
            if activities == "active":
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=game.replace("_", " ") + " | Use $help"))
            if activities == "dnd":
                await self.bot.change_presence(status=discord.Status.online.dnd, activity=discord.Game(name=game.replace("_", " ") + " | Inactive"))
            if activities == "streaming":
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name=game.replace("_", " "), url = "https://twitch.tv/primaryian210" + " | Use $help"))
            pickle.dump(game, open("game.pickle", "wb"))
            pickle.dump(activities, open("activity.pickle", "wb"))
            print("Working on it...")

        elif (spec_bot.lower() == "zelda"):
            pass

        else:
            await ctx.send("Which one do you want?")

    #----------User Nickname (WIP)--------#
    @command(help="Changes the nickname of the user who runs it.", grant_level="explicit")
    async def nick(self, ctx, *, nick :str):
        await ctx.message.delete()
        await ctx.author.edit(nick=nick)


    #-------------System Usage-------------#
    @command(help="Shows the usage of the computer the bot is running on.")
    async def usage(self, ctx, interval : int):
        val1 = random.randint(0, 256)
        val2 = random.randint(0, 256)
        val3 = random.randint(0, 256)

        colorVal = discord.Colour.from_rgb(r=val1, g=val2, b=val3)
        embed = discord.Embed(title='System Usage:', description=None, colour=colorVal)
        message = ""
        async with ctx.message.channel.typing():
            for i in range(0, 5):
                message += str(psutil.cpu_percent(interval=interval)) + "%, "
            message = message[:-2]
            embed.add_field(name="CPU Usage (%):", value=message, inline=False)
            embed.add_field(name="RAM Usage (%):", value=str(psutil.virtual_memory().percent) + "%", inline=False)
            embed.add_field(name="Time inteval (sec):", value=str(interval) + " second(s)", inline=False)
            await ctx.send(content=None, embed=embed)

    #-------------Purge-----------------#
    @command(help="A purge command for deleting every single message in a specific chat in Ian's server.", grant_level="explicit")
    async def purge(self, ctx, amount : int):
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Deleted {len(deleted)} messages")

    # #--------------move people------------#
    # @commands.command(pass_context=True, no_pm=True)
    # async def move(self, ctx, user : discord.Member, channel : str):
    #     await ctx.message.delete()
    #     if ctx.message.author.id == conf.ownerID or ctx.message.author.id == Linkconfig.ashley:
    #         if channel.lower() == "alpha":
    #             await user.move_to(ctx.guild.get_channel(Linkconfig.alpha))
    #
    #         elif channel.lower() == "beta":
    #             await user.move_to(ctx.guild.get_channel(Linkconfig.beta))
    #
    #         elif channel.lower() == "omega":
    #             await user.move_to(ctx.guild.get_channel(Linkconfig.omega))
    #
    #         elif channel.lower() == "afk":
    #             await user.move_to(ctx.guild.get_channel(Linkconfig.afk))
    #     else:
    #         ctx.send("You don't have the ability to use this command.")

    #--------------Code Length-------#
    @command(aliases=["cb", "about"])
    async def codebase(self, ctx):
        banner = pyfiglet.Figlet(font="isometric1")
        data = {
            "total": 0
        }
        for root, dirs, files in os.walk(conf.rootDir):
            for file in files:
                if file.endswith(".py"):
                    lines = 0
                    with open(os.path.join(root, file), "rb") as f:
                        for line in f:
                            lines += 1
                    data["total"] += lines
                    if file.startswith("cog_"):
                        data[file] = lines

        embed = discord.Embed(title="Link codebase", description="```" + banner.renderText("Link") + '```\nv2.1 "Bitchy Banana"', colour=ctx.message.author.colour)
        for cog, lines in data.items():
            embed.add_field(name=cog.split("_")[-1].split(".")[0].capitalize() + " Cog", value=str(lines))
        await ctx.send(content=None, embed=embed)

    #-----------------------Chat Lock---------------------------#
    @command(help="Locks the specified person out of a chat.", aliases=['cl', 'lockout'], grant_level="explicit")
    async def chatlock(self, ctx, user: discord.Member):
        await ctx.message.delete()
        if user.id == ctx.author.id:
            return await ctx.send("Sorry, you have to be at least * this smart * to run this command.\n(You can't lock yourself out of chat, idiot.)")
        if ctx.channel.permissions_for(user).send_messages:
            await ctx.channel.set_permissions(user, send_messages=False, reason="Administrative chat lockout.")
            await ctx.send("{user} has been locked out of this channel by an administrator. 🔒".format(user=user.mention))
        else:
            await ctx.channel.set_permissions(user, send_messages=True, reason="Administrative chat lockout.")
            await ctx.send("{user} has had their lockout rescinded. 🔓".format(user=user.mention))

    #---------------------Set Permissions----------------------#
    @command(grant_level="explicit", aliases=['setpermissions', 'setperm', 'permset'])
    async def set_permissions(self, ctx, member : discord.Member = None, node=None, value=None):
        print("Hi")
        if member is None:
            print("member test 1")
            return await ctx.send("You must specify the user whose permissions you want to change.")
        if member.id == self.bot.user.id:
            print("member test 2")
            return await ctx.send("Access is denied. I'll manage my own permissions, thank you very much.")
        if node is None:
            print("node test")
            return await ctx.send("You must specify the node you want to modify.")
        if value is None:
            print("value test 1")
            return await ctx.send("You must specify what value to set the node to.")
        if value not in ['allow', 'deny', 'remove']:
            print("value test 2")
            return await ctx.send("Invalid value `{value}`. It must be `allow`, `deny`, or `remove`.")
        print("hi3")
        if not permission_exists(self.bot, node):
            print("permissions test")
            return await ctx.send("Invalid permissions node `{node}`. Permissions nodes follow the format `cog.command` or `cog.*` for all commands in a cog.".format(node=node))
        member_o = Profiles.obtain(member.id)
        print("hi2")
        if value == "remove":
            try:
                member_o.acl.pop(node)
                member_o.save()
                return await ctx.send("`{node}` removed from ACL for {user}.".format(node=node, user=member.name))
            except KeyError:
                return await ctx.send("`{node}` not found in ACL for {user}.".format(node=node, user=member.name))
        for n, val in member_o.acl.items():
            if n == node:
                if val == value:
                    return await ctx.send("`{node}` is already set to `{value}` for {user}.".format(node=node, value=value, user=member.name))
        member_o.acl[node] = value
        member_o.save()
        return await ctx.send("`{node}` set to `{value}` for {user}.".format(node=node, value=value, user=member.name))

    @command()
    async def acl(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        memberobj = Profiles.obtain(member.id)
        if not memberobj.acl:
            return await ctx.send("{user} has nothing in their ACL.".format(user=member.name))
        out = "__{user}'s ACL__\n```".format(user=member.name)
        for perm_node, value in memberobj.acl.items():
            out += "'{node}' : {value}\n".format(node=perm_node, value=value)
        return await ctx.send(out + "```")

def setup(bot):
    bot.add_cog(Admin(bot))
