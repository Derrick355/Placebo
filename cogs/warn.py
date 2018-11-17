import discord
from discord.ext import commands

import json
import os

def load_user_config(member):
    with open(f'data/servers/{member.guild.id}/users.json', "r", encoding="utf-8") as doc:
        user_config = json.load(doc)
        try:
            user_config2 = user_config['users'][str(member.id)]
            if user_config2 is not None:
                pass
            return user_config
        except KeyError:
            with open(f'data/servers/{member.guild.id}/users.json', "w", encoding="utf-8") as doc:
                user_config['users'][str(member.author.id)] = user_config['default']
                json.dump(user_config, doc, indent=4)
                return user_config

def write_to_user_config(ctx, data):
    with open(f'data/servers/{ctx.guild.id}/users.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

class warn:
    def __init__(self, bot):
        self.bot = bot

    async def add_warn(self, user, ctx):
        #try:
        config = load_user_config(user)
        config['users'][str(ctx.author.id)]["warns"] += 1
        if config['users'][str(ctx.author.id)]["warns"] == 5 and ctx.guild.me.top_role > user.top_role:
            kickembed = discord.Embed(
                title=f"You were just kicked, {user.name}, from {ctx.guild.name}",
                color=0xFF0000,
            )
            kickembed.add_field(
                name="Reason", value=f"Exceeded the warn limit.", inline=True
            )
            kickembed.add_field(
                name="Time",
                value="{:%b %d, %Y - %H:%M:%S}".format(ctx.message.created_at),
                inline=True,
            )
            kickembed.set_footer(
                text="Please do not dm me, I will not respond.",
                icon_url=ctx.guild.me.avatar_url,
            )
            await user.send(embed=kickembed)
            await ctx.message.guild.kick(user, reason=f"Exceeded the warn limit.")
            await ctx.send(f"{user.name} was kicked for exceeding the warn limit.")
        elif config['users'][str(ctx.author.id)]["warns"] == 5 and ctx.guild.me.top_role <= user.top_role:
            await ctx.send(
                f"{user.name} exceeded the warn limit, but I cannot kick them."
            )
        write_to_user_config(ctx, config)
        #except Exception as e:
        #    await ctx.send(f"exception: {type(e).__name__}")

    def remove_warn(self, user, ctx):
            config = load_user_config(ctx.author)

            if config["users"][ctx.author.id]["warns"] == 0:
                return False

            elif config["users"][ctx.author.id]["warns"] < 0:
                config["users"][ctx.author.id]["warns"] = 0
                write_to_user_config(ctx, config)
                return False

            config["users"][ctx.author.id]["warns"] -= 1

            write_to_user_config(ctx, config)
            return True

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, name:discord.Member):
        #try:
        if not ctx.message.author.top_role > name.top_role:
            await ctx.send(f":no_entry: {ctx.message.author.name}, you need to have a higher role than your target.")
            return
        #f = open(f'data/{user.guild.id}/users/{user.id}.json', 'w+')
        await self.add_warn(name, ctx)
        #except Exception as e:
        #    await ctx.send(f"exception: {type(e).__name__}")

    @warn.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def add(self, ctx, name:discord.Member):
        #try:
        if name is None:
            await ctx.send(":no_entry: Could not find user.")
            return
        if not ctx.message.author.top_role > name.top_role:
            await ctx.send(f":no_entry: {ctx.message.author.name}, you need to have a higher role than your target.")
            return
        #f = open(f'data/{user.guild.id}/users/{user.id}.json', 'w+')
        await self.add_warn(name, ctx)
        # except Exception as e:
        #    await ctx.send(f"exception: {type(e).__name__}")

    @warn.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def remove(self, ctx, name:discord.Member):
        if name is None:
            await ctx.send(":no_entry: Could not find user.")
            return
        if name == ctx.author:
            await ctx.send(
                f":no_entry: {ctx.message.author.name}, you can't remove a warn from yourself."
            )
            return
        if not ctx.message.author.top_role > name.top_role:
            await ctx.send("You need to have a higher role than your target.")
            return
        success = self.remove_warn(name, ctx)
        if success:
            await ctx.send(f"Removed one warn from <@{name.id}>")
        else:
            await ctx.send(f"Error. This could be because they has no warns.")

    @warn.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def amount(self, ctx, name:discord.Member):
        if name is None:
            name = ctx.author
        if ctx.author.guild_permissions.kick_members or name != ctx.author:
            await ctx.send(f":no-entry: {ctx.author.display_name}, you don't have permission to view other's warns.")
            return
        config = load_user_config(name)
        await ctx.send(f"{name.display_name} has {config['users'][str(name.id)]['warns']} warns.", delete_after=5)


def setup(bot):
    bot.add_cog(warn(bot))