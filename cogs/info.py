import discord
from discord.ext import commands

#########################################################################
# Has commands like userinfo an serverinfo in here. All commands are    #
# purely information, nothing modifies or calls anything here, along    #
# with no math.                                                         #
#########################################################################


class info:
    def __init__(self, bot):
        self.bot = bot

    # Will return information about a specifed user.
    # Returns: Username, discriminator, status, Discord Account creation, the join date of the user to the server the command was run in, their top role on the server,
    #          and if they are playing a game or streaming on Twitch.TV, it will mention that as well (That must be enabled on a per user basis, by the user.)
    # Sets embed color to the player's highest role's color.
    @commands.command(aliases=["uinfo"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def userinfo(self, ctx, *, name=""):
        """Gets information on a mentioned user."""
        if name:
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
        else:
            user = ctx.message.author

        userinfoembed = discord.Embed(
            title=f"{user.name}#{user.discriminator} - ID:{user.id}",
            description=f"Chillin' in {user.status} status",
            colour=user.top_role.color,
        )
        userinfoembed.set_thumbnail(url=user.avatar_url)
        total_days = ctx.message.created_at - user.created_at
        userinfoembed.add_field(
            name="Joined Discord on",
            value="{:%b %d, %Y - %H:%M:%S}\nThat was {} days ago!".format(
                user.created_at, total_days.days
            ),
            inline=True,
        )
        total_days = ctx.message.created_at - user.joined_at
        userinfoembed.add_field(
            name="Joined this server on",
            value="{:%b %d, %Y - %H:%M:%S}\nThat was {} days ago!".format(
                user.joined_at, total_days.days
            ),
            inline=True,
        )
        userinfoembed.add_field(name="Top Role", value=user.top_role.name, inline=True)
        if user.activity is not None:
            if isinstance(user.activity, discord.Game):
                userinfoembed.add_field(
                    name="Currently Playing", value=user.activity.name, inline=True
                )
            if isinstance(user.activity, discord.Streaming):
                userinfoembed.add_field(
                    name="Currently Streaming",
                    value="{}\n{}".format(
                        user.activity.streaming.name, user.activity.streaming.url
                    ),
                    inline=True,
                )
        await ctx.send(embed=userinfoembed)

    # Returns information on a specifed role.
    # Provides: ID, Color, Hoisted, Position, Managed, Mentionable, and a whole lot more permissions.
    # Also changes the embed color to the role's color.
    @commands.command(aliases=["rinfo"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roleinfo(self, ctx, *, roletofind: str):
        """See information on a role said. Do not mention the role."""
        for role in ctx.message.guild.roles:
            if role.name.lower() == roletofind.lower():
                logembed = discord.Embed(title=role.name, colour=role.colour)
                logembed.add_field(name="ID", value=role.id, inline=True)
                logembed.add_field(name="Color", value=str(role.colour), inline=True)
                logembed.add_field(name="Hoisted", value=role.hoist, inline=True)
                logembed.add_field(name="Postion", value=role.position, inline=True)
                logembed.add_field(name="Managed", value=role.managed, inline=True)
                logembed.add_field(
                    name="Mentionable", value=role.mentionable, inline=True
                )
                logembed.add_field(
                    name="create_instant_invite",
                    value=role.permissions.create_instant_invite,
                    inline=True,
                )
                logembed.add_field(
                    name="kick_members",
                    value=role.permissions.kick_members,
                    inline=True,
                )
                logembed.add_field(
                    name="ban_members", value=role.permissions.ban_members, inline=True
                )
                logembed.add_field(
                    name="administrator",
                    value=role.permissions.administrator,
                    inline=True,
                )
                logembed.add_field(
                    name="manage_channels",
                    value=role.permissions.manage_channels,
                    inline=True,
                )
                logembed.add_field(
                    name="manage_guild",
                    value=role.permissions.manage_guild,
                    inline=True,
                )
                logembed.add_field(
                    name="add_reactions",
                    value=role.permissions.add_reactions,
                    inline=True,
                )
                logembed.add_field(
                    name="view_audit_log",
                    value=role.permissions.view_audit_log,
                    inline=True,
                )
                logembed.add_field(
                    name="read_messages",
                    value=role.permissions.read_messages,
                    inline=True,
                )
                logembed.add_field(
                    name="send_messages",
                    value=role.permissions.send_messages,
                    inline=True,
                )
                logembed.add_field(
                    name="send_tts_messages",
                    value=role.permissions.send_tts_messages,
                    inline=True,
                )
                logembed.add_field(
                    name="manage_messages",
                    value=role.permissions.manage_messages,
                    inline=True,
                )
                logembed.add_field(
                    name="embed_links", value=role.permissions.embed_links, inline=True
                )
                logembed.add_field(
                    name="attach_files",
                    value=role.permissions.attach_files,
                    inline=True,
                )
                logembed.add_field(
                    name="read_message_history",
                    value=role.permissions.read_message_history,
                    inline=True,
                )
                logembed.add_field(
                    name="mention_everyone",
                    value=role.permissions.mention_everyone,
                    inline=True,
                )
                logembed.add_field(
                    name="external_emojis",
                    value=role.permissions.external_emojis,
                    inline=True,
                )
                logembed.add_field(
                    name="connect", value=role.permissions.connect, inline=True
                )
                logembed.add_field(
                    name="speak", value=role.permissions.speak, inline=True
                )
                logembed.add_field(
                    name="mute_members",
                    value=role.permissions.mute_members,
                    inline=True,
                )
                logembed.add_field(
                    name="deafen_members",
                    value=role.permissions.deafen_members,
                    inline=True,
                )
                logembed.add_field(
                    name="move_members",
                    value=role.permissions.move_members,
                    inline=True,
                )
                logembed.add_field(
                    name="use_voice_activation",
                    value=role.permissions.use_voice_activation,
                    inline=True,
                )
                logembed.add_field(
                    name="change_nickname",
                    value=role.permissions.change_nickname,
                    inline=True,
                )
                logembed.add_field(
                    name="manage_nicknames",
                    value=role.permissions.manage_nicknames,
                    inline=True,
                )
                logembed.add_field(
                    name="manage_roles",
                    value=role.permissions.manage_roles,
                    inline=True,
                )
                logembed.add_field(
                    name="manage_webhooks",
                    value=role.permissions.manage_webhooks,
                    inline=True,
                )
                logembed.add_field(
                    name="manage_emojis",
                    value=role.permissions.manage_emojis,
                    inline=True,
                )
                await ctx.send(embed=logembed)
                return

    # Provides information on a server, with the server being the command it was run in.
    # Provides: Server name & ID, Date server was created, what region it's in, who the owner is, what the verification level is, it's member count,
    #           the top role on the server, it's AFK channel, and the amount of channel seperated by type, which are Voice Channels, Text Channels, and Categories.
    @commands.command(aliases=["sinfo"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def serverinfo(self, ctx):
        """See information on the current server."""
        embed = discord.Embed(
            title=f"{ctx.message.guild.name} - ID:{ctx.message.guild.id}",
            timestamp=ctx.message.created_at,
            colour=0x7289DA,
        )
        embed.set_thumbnail(url=ctx.message.guild.icon_url)
        total_days = ctx.message.created_at - ctx.message.guild.created_at
        embed.add_field(
            name="Created At",
            value="{:%b %d, %Y - %H:%M:%S}\nThat was {} days ago!".format(ctx.message.guild.created_at, total_days.days),
        )
        embed.add_field(name="Region", value=ctx.message.guild.region, inline=True)
        embed.add_field(
            name="Owner",
            value=f"{ctx.message.guild.owner.name}#{ctx.message.guild.owner.discriminator}",
            inline=True,
        )
        embed.add_field(
            name="Verification Level",
            value=ctx.message.guild.verification_level,
            inline=True,
        )
        embed.add_field(
            name="Member Count", value=len(ctx.message.guild.members), inline=True
        )
        top_role = ctx.message.guild.roles[-1]
        embed.add_field(name="Top Role", value=top_role.name, inline=True)
        embed.add_field(
            name="AFK Channel", value=ctx.message.guild.afk_channel.name, inline=True
        )
        embed.add_field(
            name="Channels",
            value=f"{len(ctx.message.guild.voice_channels)} voice channels\n{len(ctx.message.guild.text_channels)} text channels\n{len(ctx.message.guild.categories)} categories",
            inline=True,
        )
        await ctx.send(embed=embed)

    # Provides information on a message. Message must be in the bot's cache.
    # Provides: Message ID, Content, Author, Channel, if it mentioned everyone, how many people it mentioned, if it's pinned, how many channels were mentioned,
    # how many roles were mentioned, how many individual reactions there are, and how many total reactions are there.
    @commands.command(aliases=["minfo"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def messageinfo(self, ctx, messageid: int):
        """Get information on a message"""
        #channel = ctx.guild.get_channel(channelid)
        message2 = await ctx.guild.me.get_message(messageid)
        embed = discord.Embed(
            title="Message Info", description=f"ID: {messageid}", color=0x846513
        )
        embed.add_field(name="Content", value=message2.system_content, inline=False)
        embed.add_field(
            name="Author",
            value=f"{message2.author.name}#{message2.author.discriminator}",
            inline=True,
        )
        embed.add_field(name="Channel", value=message2.channel.name, inline=True)
        if message2.mention_everyone:
            embed.add_field(
                name="Mentioned Everyone", value=message2.mention_everyone, inline=True
            )
        if message2.pinned:
            embed.add_field(name="Pinned", value=message2.pinned, inline=True)
        if len(message2.mentions) > 0:
            embed.add_field(name="Mentions", value=len(message2.mentions), inline=True)
        if len(message2.channel_mentions) > 0:
            embed.add_field(
                name="Channel Mentions",
                value=len(message2.channel_mentions),
                inline=True,
            )
        if len(message2.role_mentions) > 0:
            embed.add_field(
                name="Role Mentions", value=len(message2.role_mentions), inline=True
            )
        if len(message2.reactions) > 0:
            embed.add_field(name="Indiviual Reactions", value=len(message2.reactions))
            total_reactions = 0
            for reaction in message2.reactions:
                total_reactions += reaction.count
            embed.add_field(name="Total Reactions", value=total_reactions)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(info(bot))
