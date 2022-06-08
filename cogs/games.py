import asyncio
import discord
from discord.ext import commands
import random
import os
import pickle
from conf import conf
import datetime
import math
import pytz
from cogs.orm.models import Profiles, Slots
from ext.help import localnow

from permissions import command

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Games cog started")

    #-------------Slots----------------#
    @command(help="Play a game of slots. Must bet at least 1 Rupee.")
    async def slots(self, ctx, bet):
        profile = Profiles.obtain(ctx.author.id)
        slots = Slots.obtain()
        delta = localnow() - profile.lastTime

        def render_reels(reels):
            output = ""
            for row in reels:
                output += "| ".join(row) + "|\n"
            return output

        def get_state(force=None):
            swords = list(["⚔️" for i in range(0, 58)])
            choices = ["🍋"] * 6 +  ["🍊"] * 7 + ["🍒"] * 5 + ["⚔️"] * 11 + ["⚙️"] * 3 + ["🍀"]
            slot_state = []
            for i in range(0, 3):
                row = []
                for j in range(0, 3):
                    row.append(random.choice(choices))
                slot_state.append(row)
            if force:
                slot_state[1] = [force] * 3
            else:
                if all([x == slot_state[1][0] for x in slot_state[1]]):
                    slot_state = get_state()
            return slot_state

        if random.randint(1, 1000) == 500:
            state = get_state(force="lemons")

        if bet == "all":
            bet = profile.balance
        else:
            bet = int(bet)
        if delta.total_seconds() <= 3:
             return await ctx.send("Please wait 3 seconds before running this command again.")
        if profile.balance < bet:
            return await ctx.send("You placed a bet of `{:,}".format(bet) + "` Rupees, but do not have enough. You have a balance of `{:,}".format(profile.balance) + "` Rupees in your account.")
        if bet <= 0:
            return await ctx.send("You have to bet at least 1 Rupee (Value must be positive, and not a decimal).")

        await ctx.send("`" + ctx.author.name + "` Betting {:,}".format(bet) + f" Rupees")
        msg = await ctx.send(render_reels(get_state()))

        for i in range(0, 3):
            await msg.edit(content=render_reels(get_state()))
            await asyncio.sleep(1)

        value = None

        if random.randint(1, 5) == 3:
            value = "⚔️"
            winnings = round(bet * 0.125) #1/8 winnings
        if random.randint(1, 10) == 3:
            value = "🍊"
            winnings = round(bet * 0.25) #1/4 winnings
        if random.randint(1, 23) == 3:
            value = "🍋"
            winnings = round(bet * 0.5) #1/2 winnings
        if random.randint(1, 45) == 3:
            value = "🍒"
            winnings = round(bet * 2.5) #3/2 winnings
        if random.randint(1, 75) == 3:
            value = "⚙️"
            winnings = round(bet * 3.0)#4/2 winnings
        if random.randint(1, 200) == 3:
            value = "🍀"
            winnings = bet + slots.jackpot
        if value is None:
            winnings = 0

        await msg.edit(content=render_reels(get_state(force=value)))

        if winnings == 0:
            profile.balance -= bet
            slots.jackpot += bet
            await ctx.send("`" + ctx.author.name + "` You lost!!")
        elif value == "🍀":
            profile.balance += winnings
            await ctx.send(file=discord.File(conf.imgDir + 'slots_jackpot.png'))
            await ctx.send(f'{ctx.author.mention} Congratulations! You won the jackpot of {"{:,}".format(slots.jackpot)} rupees!')
            slots.jackpot = slots.DEFAULT_JACKPOT
        else:
            profile.balance += winnings
            await ctx.send(f'You won {"{:,}".format(winnings)} rupees!')

        profile.lastTime = localnow()
        profile.save()
        slots.save()


    #-------------Currency Handling--------------#
    @command(help="Adds or removes Rupees", grant_level="explicit")
    async def rupee(self, ctx, user : discord.Member, amount : int=None):
        profile = Profiles.obtain(user.id)
        profile.balance += amount
        await ctx.send("Added `{:,}".format(amount) + "` Rupee(s) to `" + str(user.name) + "`.")
        profile.save()

    #---------------Rock, Paper, Scissors----------#
    @command(help="Play a game of Rock, Paper, Scissors.")
    async def rps(self, ctx, bet : int, choice : str):
        profile = Profiles.obtain(ctx.message.author.id)
        choices = ["rock", "paper", "scissors"]

        if bet <= 0:
            await ctx.send("You must bet at least 1 Rupee, and must be a whole, positive, number.")
        elif bet > 500:
            await ctx.send("Bet can't exceed 500 Rupees.")
        else:
            if bet > profile.balance:
                await ctx.send("You don't have that amount of Rupees to bet.")
            else:
                if choice not in choices:
                    await ctx.send("Enter either rock, paper, or scissors.")
                else:
                    bot_choice = random.choice(choices)
                    winnings = bet * 2

                    await ctx.send("You chose `" + choice + "`\nBot chose `" + bot_choice + "`")
                    if bot_choice == choice:
                        await ctx.send("It's a tie!")
                    elif bot_choice == 'rock' and choice == 'scissors':
                        await ctx.send("Bot wins! You lost {:,}".format(bet) + " Rupees!")
                        profile.balance -= bet
                    elif bot_choice == 'scissors' and choice == 'paper':
                        await ctx.send("Bot wins! You lost {:,}".format(bet) + " Rupees!")
                        profile.balance -= bet
                    elif bot_choice == 'paper' and choice == 'rock':
                        await ctx.send("Bot wins! You lost {:,}".format(bet) + " Rupees!")
                        profile.balance -= bet
                    elif choice == 'rock' and bot_choice == 'scissors':
                        await ctx.send("You win! You recieved {:,}".format(winnings) + " Rupees!")
                        profile.balance += winnings
                    elif choice == 'scissors' and bot_choice == 'paper':
                        await ctx.send("You win! You recieved {:,}".format(winnings) + " Rupees!")
                        profile.balance += winnings
                    else:
                        if choice == 'paper' and bot_choice == 'rock':
                            await ctx.send("You win! You recieved {:,}".format(winnings) + " Rupees!")
                    profile.save()


    #--------------Coin Flip---------------#
    @command(help="Place a bet on a coin flip", aliases=["coin", "cf"])
    async def coinflip(self, ctx, pick : str, bet : int):
        profile = Profiles.obtain(ctx.message.author.id)
        coin = ["heads", "tails"]

        if bet > profile.balance:
            await ctx.send("You don't have that many Rupees in your balance.")
        elif bet > 250:
            await ctx.send("Your bet can't exceed 250 Rupees.")
        else:
            if pick not in coin:
                await ctx.send("Choose either heads or tails.")
            else:
                choice = random.choice(coin)
                winnings = bet + round((bet / 0.5))

                await ctx.send("You chose `" + pick + "`\nThe coin landed on `" + choice + "`")

                if pick == choice:
                    await ctx.send("You win!\nEarned `" + str(winnings) + "` Rupees!")
                    profile.balance += winnings
                else:
                    await ctx.send("You lost!")
                    profile.balance -= bet
                profile.save()

    #------------Dailies-------------#
    @command(help="Does nothing yet. Recieve daily Rupee amount from the bot.", aliases=["dailies"])
    async def daily(self, ctx):
        profile = Profiles.obtain(ctx.message.author.id)
        delta = localnow() - profile.dailyLastTime

        if delta.total_seconds() >= 86400:
            profile.balance += 7500
            profile.dailyLastTime = localnow()
            profile.save()
            await ctx.send("Claimed 7,500 Rupees. Come back in 24 hours to claim it again.")
        else:
            await ctx.send("`" + ctx.author.name + "` please wait 24 hours before claiming again.")

    @command()
    async def jackpot(self, ctx):
        slots = Slots.obtain()
        await ctx.send(f'The current jackpot is {"{:,}".format(slots.jackpot)} rupees')


    @command(help="Clears the jackpot of a certain amount.", grant_level="explicit")
    async def clean_jackpot(self, ctx, amount : int):
        slots = Slots.obtain()
        slots.jackpot -= amount
        await ctx.send("Removed {:,}".format(amount) + " rupees from the jackpot.")
        slots.save()

"""
    @commands.command(help="Emulates a Blackjack dealer.")
    async def blackjack(self, ctx):
        QUARTER_DECK = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

        hand= []

        hand.append(random.choice(QUARTER_DECK))
        hand.append(random.choice(QUARTER_DECK))

        while True:
            if sum(hand) < 17:
                await ctx.send("Hitting with: " + str(sum(hand)))
                new_card = random.choice(QUARTER_DECK)
                if new_card == 11 and sum(hand) + 11 > 21:
                    new_card = 1
                hand.append(new_card)
                await ctx.send("Dealer got: " + str(new_card))
            elif sum(hand) >= 17 and sum(hand) <= 21:
                if sum(hand) == 21 and len(hand) == 2:
                    await ctx.send("BLACKJACK!")
                else:
                    await ctx.send("Staying with: " + str(sum(hand)))
                    break
            elif sum(hand) > 21:
                await ctx.send("BUST with: " + str(sum(hand)))
                break
            await asyncio.sleep(1)
"""
def setup(bot):
    bot.add_cog(Games(bot))
