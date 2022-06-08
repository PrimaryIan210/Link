import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import os
import random
from conf import conf

from permissions import command


class Audio(commands.Cog):
    @command()
    async def connect(self, ctx):
        self.voice = await ctx.author.voice.channel.connect()

    @command()
    async def disconnect(self, ctx):
        await self.voice.disconnect()

    @command()
    async def clip(self, ctx, *, clipname : str):
        self.voice = await ctx.author.voice.channel.connect()
        self.voice.play(discord.FFmpegPCMAudio(os.path.join(conf.clipDir, clipname + ".mp3")), after=lambda e: print('done', e))
        vc = ctx.voice_client
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.75
        while self.voice.is_playing():
            await asyncio.sleep(0.1)
        await self.voice.disconnect()

    @command()
    async def tts(self, ctx, *, words : str):
        self.voice = await ctx.author.voice.channel.connect()
        print("espeak -w " + conf.tempDir + "disck.wav \"" + words + "\"")
        os.system("espeak -w " + os.path.join(conf.tempDir, "disck.wav") + " \"" + words + "\"")
        self.voice.play(discord.FFmpegPCMAudio(os.path.join(conf.tempDir, "disck.wav")), after=lambda e: print('done', e))
        while self.voice.is_playing():
            await asyncio.sleep(0.1)
        await self.voice.disconnect()

def setup(bot):
    bot.add_cog(Audio(bot))
