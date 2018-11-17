from discord.ext import commands
import discord

import traceback
import sys
import math

"""
If you are not using this inside a cog, add the event decorator e.g:
@bot.event
async def on_command_error(ctx, error)
For examples of cogs see:
Rewrite:
https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
Async:
https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5
This example uses @rewrite version of the lib. For the async version of the lib, simply swap the places of ctx, and error.
e.g: on_command_error(self, error, ctx)
For a list of exceptions:
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#errors
"""


class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        if isinstance(error, commands.NotOwner):
            await ctx.send("You are not the owner of the bot.")
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f"{ctx.command} has been disabled.")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(
                    f"{ctx.command} can not be used in Private Messages."
                )
            except:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if (
                ctx.command.qualified_name == "tag list"
            ):  # Check if the command being invoked is 'tag list'
                return await ctx.send("I could not find that member. Please try again.")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You're missing a required argument. Please retry with all needed arguments.\nIf you aren't sure about the arguments, use ^help.")
            return

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("You have too many arguments. Please retry only the needed arguments.\nIf you aren't sure about the arguments, use ^help.")
            return

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"That command is on cooldown. Try again in {math.ceil(error.retry_after)} seconds.")
            return

        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', " ").replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            await ctx.send(_message)
            return

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', " ").replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'I need the **{}** permission(s) to use this command.'.format(fmt)
            await ctx.send(_message)
            return

        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
            return


        # All other Errors not returned come here... And we can just print the default TraceBack.
        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    """Below is an example of a Local Error Handler for our command do_repeat"""

    @commands.command(name="repeat", aliases=["mimic", "copy"])
    @commands.is_owner()
    async def do_repeat(self, ctx, *, inp: str):
        """A simple command which repeats your input!
        inp  : The input to be repeated"""

        await ctx.send(inp)

    @do_repeat.error
    async def do_repeat_handler(self, ctx, error):
        """A local Error Handler for our command do_repeat.
        This will only listen for errors in do_repeat.
        The global on_command_error will still be invoked after."""

        # Check if our required argument inp is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "inp":
                await ctx.send("You forgot to give me input to repeat!")


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))