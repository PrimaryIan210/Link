import discord
import asyncio
import random
from discord.ext import commands

class LeveledEntity:
    def __init__(self):
        self.exp = 0

    @property
    def level(self):
        return int(((-35) + sqrt((8 * self.exp) + 1225)) / 10 + 1)

    def set_exp_by_level(self, level):
        self.exp = 12.5 * ((level - 1)**2) + 87.5 * (level - 1)

class Player(LeveledEntity):
    def __init__(self, usd):
        super().__init__()
        self.uid = uid

class Enemy(LeveledEntity):
    def __init__(self, player):
        self.player_level = player.level
        self.calculate_level()

    def calculate_level(self):
        level_range = {}
        level_range['0'] = player.level - 3 if player.level - 3 > 0 else 0
        level_range['1'] = player.level + 3
        set_level = random.randint(level_range['0'], level_range['1'])
        self.set_exp_by_level(set_level)

    def exp_on_death(self):
        divisor = 10
        if self.player_level > self.level:
            divisor -= (self.player_level - self.level)
        else:
            divisor += (self.level - self.player_level)
        return round(self.exp / divisor)
