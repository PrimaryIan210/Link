from cogs.orm.models import Profiles

from discord.ext import commands

class Command(commands.Command):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self.grant_level = kwargs['grant_level'] if 'grant_level' in kwargs else 'implicit'
        self.add_check(self.permissions_check)

    def node(self, bot):
        for command in bot.commands:
            if command.qualified_name == self.qualified_name:
                return command.cog.qualified_name.lower() + "." + self.qualified_name.lower()

    def permissions_check(self, ctx):
        member = Profiles.obtain(ctx.author.id)
        cog, command = self.node(ctx.bot).split(".")

        for node, value in member.acl.items():
            if (node == cog + "." + command) or (node == cog + ".*"):
                if value == "deny":
                    return False

        if self.grant_level != "implicit":
            for node, value in member.acl.items():
                if (node == cog + "." + command) or (node == cog + ".*"):
                    if value == "allow":
                        return True
                elif node == "bot.*":
                    if value == "allow":
                        return True
                else:
                    pass
            return False
        else:
            return True

def command(name=None, cls=None, **attrs):
    if cls is None:
        cls = Command

    def decorator(func):
        if isinstance(func, Command):
            raise TypeError("Callback is already a command.")
        return cls(func, name=name, **attrs)
    return decorator

def permission_exists(bot, node):
    if node == "bot.*":
        return True

    for cog in bot.cogs:
        if node == cog.lower() + ".*":
            return True

    for command in bot.commands:
        try:
            if command.node(bot) == node:
                return True
        except AttributeError:
            pass
    return False
