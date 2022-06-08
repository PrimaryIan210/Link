import asyncio
import discord
from discord.ext import commands
import random
import os
import pickle
from conf import conf
from cogs.orm.models import Profiles

from permissions import command

from PIL import Image, ImageOps
from io import BytesIO
import requests

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Profile cog started")
    #----------Show Profile--------------#
    @command(help="Shows profile of the user.")
    async def profile(self, ctx, *, user : discord.Member=None):
        user = ctx.author if not user else user
        roles = [role.name for role in user.roles if '\u2002' not in role.name]

        prof = Profiles.obtain(user.id)

        embed = discord.Embed(title=user.name, description=None, colour=user.colour)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Nickname:", value=user.nick)

        embed.add_field(name="Joined " + ctx.message.guild.name + ":", value=user.joined_at.strftime("%m/%d/%Y %H:%M:%S"))
        embed.add_field(name="Role(s):", value=str(roles), inline=False)

        embed.add_field(name="Last Daily Claim (Displayed in UTC):", value=str(prof.dailyLastTime.strftime("%m/%d/%Y %H:%M:%S")), inline=False)

        embed.add_field(name="Current Balance:", value="{:,}".format(prof.balance) + " Rupees")
        #embed.add_field(name="Debt:", value="{:,}".format(prof.debt) + " Rupees")
        await ctx.send(embed=embed)

    @command(help="The new profile system test. Exclusive")
    async def new_profile(self, ctx, user : discord.Member=None):
        user = ctx.author if not user else user

        def construct(self, avatar):
            response = requests.get(user.avatar_url)
            img = Image.open(BytesIO(response.content)).convert("RGBA")
            mask = Image.open(os.path.join(Linkconfig.imageDir + "profile/", "profile_picture_mask.png")).convert('L')
            out = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
            out.putalpha(mask)
            out = out.resize(300, 300)
            background = Image.open(os.path.join(Linkconfig.imageDir + "profile/", "profile_picture_default_background")).resize(1920, 1080)
            profile = Image.new(mode="RGBA", size=(1920, 1080))

        await ctx.send(file=discord.File(construct(self, user)))

def setup(bot):
    bot.add_cog(Profile(bot))
