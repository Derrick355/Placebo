import discord
from discord.ext import commands

#########################################################################
# For self-assign shit. It has to be hardcoded because I'm too lazy to  #
# make it modifyable via commands.                                      #
#########################################################################


class selfassign:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def react(self, ctx, message_id: int, emoji_name: str):
        """Have the bot react to any message. Required permission: manage_messages"""
        to_react = await ctx.message.channel.get_message(message_id)
        for server_emoji in ctx.guild.emojis:
            if server_emoji.name == emoji_name:
                await to_react.add_reaction(server_emoji)
                break

    async def on_raw_reaction_add(self, infoonreaction):
        if infoonreaction.message_id == 477599896380112897:
            guild = self.bot.get_guild(infoonreaction.guild_id)

            user = guild.get_member(infoonreaction.user_id)
            if not user:
                user = self.bot.get_user(infoonreaction.user_id)

            if infoonreaction.emoji.name == "Steam":
                steamrole = discord.utils.get(guild.roles, name="Steam")
                await user.add_roles(steamrole)
            if infoonreaction.emoji.name == "Nintendo":
                nintendorole = discord.utils.get(guild.roles, name="Nintendo")
                await user.add_roles(nintendorole)
            if infoonreaction.emoji.name == "PlayStation":
                psrole = discord.utils.get(guild.roles, name="PlayStation")
                await user.add_roles(psrole)
            if infoonreaction.emoji.name == "XBOX":
                xboxrole = discord.utils.get(guild.roles, name="XBOX")
                await user.add_roles(xboxrole)
        if infoonreaction.message_id == 477885283094888448:
            guild = self.bot.get_guild(infoonreaction.guild_id)

            user = guild.get_member(infoonreaction.user_id)
            if not user:
                user = self.bot.get_user(infoonreaction.user_id)

            if infoonreaction.emoji.name == "helYEA":
                freegamerole = discord.utils.get(guild.roles, name="Free Games")
                await user.add_roles(freegamerole)

        if infoonreaction.message_id == 484148541611311124:
            guild = self.bot.get_guild(infoonreaction.guild_id)
            user = guild.get_member(infoonreaction.user_id)
            if not user:
                user = self.bot.get_user(infoonreaction.user_id)

            if infoonreaction.emoji.name == "paul":
                timelordrole = discord.utils.get(guild.roles, name="Timelord")
                await user.add_roles(timelordrole)
                await user.send(
                    "Thanks for agreeing to our rules. Please be warned, if you unreact to this message, all your roles will be immediatly revoked."
                )

    async def on_raw_reaction_remove(self, infoonreaction):
        if infoonreaction.message_id == 477599896380112897:
            guild = self.bot.get_guild(infoonreaction.guild_id)

            user = guild.get_member(infoonreaction.user_id)
            if not user:
                user = self.bot.get_user(infoonreaction.user_id)
            if infoonreaction.emoji.name == "Steam":
                steamrole = discord.utils.get(guild.roles, name="Steam")
                await user.remove_roles(steamrole)
            if infoonreaction.emoji.name == "Nintendo":
                nintendorole = discord.utils.get(guild.roles, name="Nintendo")
                await user.remove_roles(nintendorole)
            if infoonreaction.emoji.name == "PlayStation":
                psrole = discord.utils.get(guild.roles, name="PlayStation")
                await user.remove_roles(psrole)
            if infoonreaction.emoji.name == "XBOX":
                xboxrole = discord.utils.get(guild.roles, name="XBOX")
                await user.remove_roles(xboxrole)

        if infoonreaction.message_id == 477198301620600842:
            guild = self.bot.get_guild(infoonreaction.guild_id)

            user = guild.get_member(infoonreaction.user_id)
            if not user:
                user = self.bot.get_user(infoonreaction.user_id)

            if infoonreaction.emoji.name == "helYEA":
                freegamerole = discord.utils.get(guild.roles, name="Free Games")
                await user.remove_roles(freegamerole)

        if infoonreaction.message_id == 484148541611311124:
            guild = self.bot.get_guild(infoonreaction.guild_id)
            user = guild.get_member(infoonreaction.user_id)
            if not user:
                user = self.bot.get_user(infoonreaction.user_id)

            if infoonreaction.emoji.name == "paul":
                for role in user.roles:
                    if role.name != "@everyone":
                        try:
                            await user.remove_roles(role)
                        except discord.errors.Forbidden:
                            print("error.")
                await user.send(
                    "You disagreed to our rules. As such, every role has been revoked."
                )


def setup(bot):
    bot.add_cog(selfassign(bot))
