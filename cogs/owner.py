import discord
from discord.ext import commands
import time

#########################################################################
# Commands like move and unload_command can be found here.              #
# All the commands found here can only be run by the owner of the bot's #
# account.                                                              #
#########################################################################


def config_load(m):
    with open(f"data/servers/{m.guild.id}/config.json", "r", encoding="utf-8") as doc:
        return doc


class owner:
    def __init__(self, bot):
        self.bot = bot

    # Move a user from one voice channel to another. Use like so: move [channelID] <user>
    # If no user specified, will move the message sender
    @commands.command()
    @commands.is_owner()
    async def move(self, ctx, channelid, name=None):
        user = None
        channel_to_move = None
        for channel in ctx.guild.voice_channels:
            if channel.id == int(channelid):
                channel_to_move = channel
                break
        if name is not None:
            try:
                user = ctx.message.mentions[0]
            except IndexError:
                user = ctx.guild.get_member_named(name)
            if not user:
                user = ctx.guild.get_member(int(name))
            if not user:
                user = self.bot.get_user(int(name))
            if not user:
                await ctx.send(":no_entry: Could not find user.")
                return
        # channel_to_move = ctx.guild.get_channel(channelid)
        if user is None:
            user = ctx.message.author
        await user.edit(voice_channel=channel_to_move)
        await ctx.send(f":white_check_mark: Moved!")

    # Bot will simply repeat an input.
    @commands.command(aliases=["speak"])
    @commands.is_owner()
    async def say(self, ctx, *, message):
        """Bot will say what you want it to. Required permission: manage_guild"""
        await ctx.message.delete()
        await ctx.send(message)

    # Allows for the quick unloading of commands if a related error pops up while trying to load a cog.
    @commands.command()
    @commands.is_owner()
    async def unload_command(self, ctx, command):
        self.bot.remove_command(command)

    @commands.command()
    @commands.is_owner()
    async def restore(self, ctx, command):
        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name="Moderator"))

def setup(bot):
    bot.add_cog(owner(bot))
