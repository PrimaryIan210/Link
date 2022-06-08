import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
import pickle
import Linkconfig
import random
#from cogs.orm.models import Pokemon
import pokebase as pokemon

class Pokedex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Pokedex cog started")

    @commands.command()
    async def dexinfo(self, ctx, reqArg):
        pokemoninfo = pokemon.pokemon(reqArg)
        #val1 = random.randint(0, 256)
        #val2 = random.randint(0, 256)
        #val3 = random.randint(0, 256)

        #colorVal = discord.Colour.from_rgb(r=val1, g=val2, b=val3)
        embed = discord.Embed(title=(pokemoninfo.name).capitalize(), description=None)

        embed.add_field(name="Dex Number", value=str(pokemoninfo.id))
        embed.add_field(name="Type(s)", value=str(pokemoninfo.types).replace("{'slot': 1, 'type': {'name': ", "").replace("{'slot': 2, 'type': {'name': ", ""))
        embed.add_field(name="Height", value=str(pokemoninfo.height) + " Centimeters")
        embed.add_field(name="Weight", value=str(pokemoninfo.weight) + " Kilograms")

        await ctx.send(content=None, embed=embed)

        """if isinstance(reqArg, str):
            await ctx.send(pokemoninfo.name)
        else:
            await ctx.send("Invalid")"""

    """@commands.command(pass_context=True, no_pm=True, help="Adds Pokédex entry to the bot.")
    async def adddexinfo(self, ctx, pokemonname : str, dexnumber : int):
        if ctx.message.author.id == Linkconfig.me:
            await ctx.message.delete()
            pokemon = Pokemon(pokemonname, dexnumber)
            pokemon.save()

        else:
            await ctx.send("You do not have the ability to use this command")

    @commands.command()
    async def dexinfo(self, ctx, reqArg):
        try:
            if reqArg.isdigit():
                pokemon = Pokemon.obtain(number=int(reqArg))
                await ctx.send(str(pokemon.dexnumber))
                await ctx.send(pokemon.pokemonname)

            else:
                pokemon = Pokemon.obtain(name=reqArg)
                await ctx.send(str(pokemon.dexnumber))
                await ctx.send(pokemon.pokemonname)

        except FileNotFoundError:
            return await ctx.send("No pokemon with that name or number was found.")"""

def setup(bot):
    bot.add_cog(Pokedex(bot))
