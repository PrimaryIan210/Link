import asyncio
import discord
from discord.ext import commands
import random
from conf import conf
from cogs.orm.models import PlayerData
from cogs.RPG.enemy import Enemy

from permissions import command

class RPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabledUsers = []

    # @commands.command()
    # async def rpg(self, ctx):
    #     player = PlayerData.obtain(ctx.author.id)
    #     if not player.rpg_channel:
    #         player.rpg_channel = ctx.message.channel.id
    #         await ctx.send("enabled")
    #     else:
    #         player.rpg_channel = None
    #         await ctx.send("disabled")
    #     player.save()
    #
    # @commands.command()
    # async def createcharacter(self, ctx, user : discord.Member=None):
    #     user = ctx.author if not user else user
    #     player = Player.obtain(user.id)
    #
    #     if ctx.message.author.id == Linkconfig.me:
    #         player.save()
    #         await ctx.send("Created successfully")
    #     else:
    #         await ctx.send("You don't have the ability to use this command. Especially, because it only works for Ian right now, as well as does nothing.")
    #
    # @commands.command()
    # async def stats(self, ctx, user : discord.Member=None):
    #     user = ctx.author if not user else user
    #     player = Player.obtain(user.id)
    #
    #     embed = discord.Embed(title=user.name, description="World of Meridian", colour=user.colour)
    #     embed.set_thumbnail(url=user.avatar_url)
    #     embed.add_field(name="Class:", value=player.character)
    #     embed.add_field(name="Level:", value=str(int(player.level)))
    #     embed.add_field(name="EXP.:", value=str(int(player.current_exp)))
    #     embed.add_field(name="Next Level:", value=str(int(player.next_level_exp)))
    #     embed.add_field(name="HP:", value=str(player.hp))
    #     embed.add_field(name="MP:", value=str(player.mp))
    #     embed.add_field(name="ATK:", value=str(player.atk))
    #     await ctx.send(embed=embed)
    #
    # @commands.command()
    # async def generate_enemy(self, ctx):
    #     enemy = ["Orc", "Dragon", "Spriggans", "Fallen Angel", "Bokoblin", "Moblin"]
    #     await ctx.send("The enemy before you is a " + random.choice(enemy))
    #
    # async def process(self, ctx):
    #     player = PlayerData.obtain(ctx.author.id)
    #     if player.rpg_channel == ctx.channel.id:
    #         await ctx.send("hi")



#exp equation 300 + sqrt(x)
#stat equation somethingsomething + sqrt(y)
#damage formula attack*(100/(100+defense))
def setup(bot):
    bot.add_cog(RPG(bot))
