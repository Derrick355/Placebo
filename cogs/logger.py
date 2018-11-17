import discord
from discord.ext import commands

import datetime
import json
import time
#########################################################################
# All of these will log to a text channel that was specified by the     #
# server owner via the settings command.                                #
# All message-related logs will ony log if the message is in the bot's  #
# cache.                                                                #
#########################################################################

class logger:
    def __init__(self, bot):
        self.bot = bot
    
    # To open the config file.
    def config_load(self, guild_id):
        with open(f'data/servers/{guild_id}/config.json', 'r', encoding='utf-8') as doc:
            return json.load(doc)

    # Whenever a message gets deleted, it will log it in an appropiate mod logs channel as set in the server's config file.
    async def on_message_delete(self, message):
        config = self.config_load(message.guild.id)
        if message.channel.id == int(config['modlogsid']):
            return
        logembed = discord.Embed(title=f"{message.author.name}#{message.author.discriminator}'s message was deleted", description=f"Server: {message.guild.name}", color=0xff0000)
        if message.content != '':
            logembed.add_field(name="Contents", value=message.content)
        if message.attachments is not None:
            for attachment in message.attachments:
                logembed.add_field(name="Attachment", value=f'WARNING; Links on here could be malicious. Watch out.\nImages from deleted messages only last from 0 minutes to around 5.\n{attachment.proxy_url}')
        logchannel = self.bot.get_channel(int(config['modlogsid']))
        logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
        await logchannel.send(embed=logembed)

    # Logs if a message was editted. Will only work for the message in the bot's cache
    async def on_message_edit(self, messagebefore, messageafter):
        if len(messageafter.embeds) == 0:
            logembed = discord.Embed(title=f"{messageafter.author.name}#{messageafter.author.discriminator}'s message was editted", description=f"Server: {messageafter.guild.name}", color=0x00ffff)
            if messagebefore.content != messageafter.content:
                logembed.add_field(name="Before Contents", value=messagebefore.content, inline=False)
                logembed.add_field(name="After Contents", value=messageafter.content, inline=False)
            if messagebefore.pinned != messageafter.pinned:
                logembed.add_field(name="Pinned", value=messageafter.pinned)
            config = self.config_load(messageafter.guild.id)
            logchannel = self.bot.get_channel(int(config['modlogsid']))
            logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
            await logchannel.send(embed=logembed)

    # If a channel was created, will log it. Using isinstance, the bot will denote if the newly created channel is a text, voice, or category.
    async def on_guild_channel_create(self, channel):
        if isinstance(channel, discord.TextChannel):
            logembed = discord.Embed(title="A text channel was created", description=f'Name: {channel.name}', color=0x4f8803)
            logembed.add_field(name="Created at", value=channel.created_at, inline=True)
            config = self.config_load(channel.guild.id)
            logchannel = self.bot.get_channel(int(config['modlogsid']))
            logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
            await logchannel.send(embed=logembed)
        if isinstance(channel, discord.VoiceChannel):
            logembed = discord.Embed(title="A voice channel was created", description=f'Name: {channel.name}', color=0x4f8803)
            logembed.add_field(name="Created at", value=channel.created_at, inline=True)
            config = self.config_load(channel.guild.id)
            logchannel = self.bot.get_channel(int(config['modlogsid']))
            logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
            await logchannel.send(embed=logembed)
        if isinstance(channel, discord.CategoryChannel):
            logembed = discord.Embed(title="A category was created", description=f'Name: {channel.name}', color=0x4f8803)
            logembed.add_field(name="Created at", value=channel.created_at, inline=True)
            config = self.config_load(channel.guild.id)
            logchannel = self.bot.get_channel(int(config['modlogsid']))
            logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
            await logchannel.send(embed=logembed)

    # Same as channel create, but will log when a channel is deleted.
    async def on_guild_channel_delete(self, channel):
        if isinstance(channel, discord.TextChannel):
            logembed = discord.Embed(title="A text channel was deleted", description=f'Name: {channel.name}', color=0x4f8803)
            config = self.config_load(channel.guild.id)
            logchannel = self.bot.get_channel(int(config['modlogsid']))
            logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
            await logchannel.send(embed=logembed)
        if isinstance(channel, discord.VoiceChannel):
            logembed = discord.Embed(title="A voice channel was deleted", description=f'Name: {channel.name}', color=0x4f8803)
            config = self.config_load(channel.guild.id)
            logchannel = self.bot.get_channel(int(config['modlogsid']))
            logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
            await logchannel.send(embed=logembed)
        if isinstance(channel, discord.CategoryChannel):
            logembed = discord.Embed(title="A category was deleted", description=f'Name: {channel.name}', color=0x4f8803)
            config = self.config_load(channel.guild.id)
            logchannel = self.bot.get_channel(int(config['modlogsid']))
            logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
            await logchannel.send(embed=logembed)

    # If a channel is updated in certain ways, it will log it. Using the Advanced FUKU AI™, it can tell what was changed and will put the change
    # in the sent embed.
    async def on_guild_channel_update(self, channelbefore, channelafter):
        supported = False
        if isinstance(channelafter, discord.TextChannel):
            logembed = discord.Embed(title="A text channel was updated", description=f"Name: {channelafter.name}", color=0xf01bfe)
            if channelbefore.name != channelafter.name:
                logembed.add_field(name="Name", value=f"Before:\n{channelbefore.name}\nAfter:\n{channelafter.name}", inline=False)
                supported = True
            if channelbefore.position != channelafter.position:
                logembed.add_field(name="Position", value=f'Before:\n{channelbefore.position}\nAfter:\n{channelafter.position}', inline=False)
                supported = True
            if supported:
                config = self.config_load(channelafter.guild.id)
                logchannel = self.bot.get_channel(int(config['modlogsid']))
                logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
                await logchannel.send(embed=logembed)
        if isinstance(channelafter, discord.VoiceChannel):
            logembed = discord.Embed(title="A voice channel was updated", description=f"Name {channelafter.name}", color=0xf01bfe)
            if channelbefore.name != channelafter.name:
                logembed.add_field(name="Name", value=f"Before:\n{channelbefore.name}\nAfter:\n{channelafter.name}", inline=False)
                supported = True
            if channelbefore.position != channelafter.position:
                logembed.add_field(name="Position", value=f'Before:\n{channelbefore.position}\nAfter:\n{channelafter.position}', inline=False)
                supported = True
            if supported:
                config = self.config_load(channelafter.guild.id)
                logchannel = self.bot.get_channel(int(config['modlogsid']))
                logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
                await logchannel.send(embed=logembed)

    # When a user joins, will log it. Also will mention the new user count.
    async def on_member_join(self, member):
        logembed = discord.Embed(title="A user joined this server.", description=f"Name: {member.name}#{member.discriminator}\nNew player count: {len(member.guild.members)}", color=0xffffff)
        config = self.config_load(member.guild.id)
        logchannel = self.bot.get_channel(int(config['modlogsid']))
        logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
        await logchannel.send(embed=logembed)
        if config['enablenewmemberchannel']:
            thatchannel = self.bot.get_channel(int(config['newmemberchannel']))
            new_member_message = config['newmembermessage'].format(member.guild.name, member.id)
            await thatchannel.send(new_member_message)

    # Same as above, but for when a user left.
    async def on_member_remove(self, member):
        logembed = discord.Embed(title="A user left this server.", description=f"Name: {member.name}#{member.discriminator}\nNew player count: {len(member.guild.members)}", color=0x434343)
        config = self.config_load(member.guild.id)
        logchannel = self.bot.get_channel(int(config['modlogsid']))
        logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
        await logchannel.send(embed=logembed)
        if config['enablememberleftmessage']:
            thatchannel = self.bot.get_channel(int(config['newmemberchannel']))
            member_left_message = config['leftguildmessage'].format(member.display_name)
            await thatchannel.send(member_left_message)

    # Whenever a user updates thier account by changing their avatar or display name it will log it.
    async def on_member_update(self, memberbefore, memberafter):
        supported = False
        logembed = discord.Embed(title="A user updated their account", description=f"Name: {memberafter.name}#{memberafter.discriminator}", color=0xc54814)
        if memberbefore.avatar_url != memberafter.avatar_url:
            logembed.add_field(name="Avatar", value=f"Before:\n{memberbefore.avatar_url}\nAfter:\n{memberafter.avatar_url}", inline=False)
            supported = True
        if memberbefore.display_name != memberafter.display_name:
            logembed.add_field(name="Display Name", value=f"Before:\n{memberbefore.display_name}\nAfter:\n{memberafter.display_name}")
            supported = True
        if supported:
            config = self.config_load(memberafter.guild.id)
            logchannel = self.bot.get_channel(int(config['modlogsid']))
            logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
            await logchannel.send(embed=logembed)

    # When a user changes their voice state, either forced or not, it will be logged.
    # Due to the way the API works, I cannot log who forcefully muted/deafened or moved a user, but I can tell when A user was forceully muted or deafened by another user.
    async def on_voice_state_update(self, member, beforevs, aftervs):
        if (member.id == 146151306216734720 or member.id == 271456944055779328) and aftervs.channel.id != 500042125149208586:
            await member.edit(voice_channel=beforevs.channel)
        #if member.id == 271456944055779328 and aftervs.channel.id == 477199785015640065:
        #    thatchannel2 = self.bot.get_channel(477199037502718002)
        #    time.sleep(1)
        #    await member.edit(voice_channel=thatchannel2)
        logembed = discord.Embed(title='A user updated their voice state', description=f'Name: {member.name}#{member.discriminator}', color=0x543346)
        if beforevs.channel != aftervs.channel:
            if beforevs.channel is None:
                logembed.add_field(name="User joined a Voice Channel", value=f"Joined channel {aftervs.channel.name}")
            elif aftervs.channel is None:
                logembed.add_field(name="User left a Voice Channel", value=f"Left channel {beforevs.channel.name}")
            else:
                logembed.add_field(name='User changed voice channels', value=f'Left {beforevs.channel.name}\nJoined {aftervs.channel.name}')
        elif beforevs.deaf != aftervs.deaf:
            if beforevs.deaf:
                logembed.add_field(name=':x:', value="User was forcefully undeafened", inline=False)
            if aftervs.deaf:
                logembed.add_field(name=':x:', value="User was forcefully deafened", inline=False)
            #if member.id == 146151306216734720 and aftervs.deaf == True: # This was to prevent a certain user from messing with me.
            #    await member.edit(deafen=False)
        elif beforevs.mute != aftervs.mute:
            if beforevs.mute:
                logembed.add_field(name=':x:', value="User was forcefully unmuted", inline=False)
            if aftervs.mute:
                logembed.add_field(name=':x:', value="User was forcefully muted", inline=False)
            #if member.id == 146151306216734720 and aftervs.mute == True: # Same as last comment.
            #    await member.edit(mute=False)
        elif beforevs.self_mute != aftervs.self_mute:
            if beforevs.self_mute:
                logembed.add_field(name=':x:', value="User unmuted themselves", inline=False)
            if aftervs.self_mute:
                logembed.add_field(name=':x:', value="User muted themselves", inline=False)
        elif beforevs.self_deaf != aftervs.self_deaf:
            if beforevs.self_deaf:
                logembed.add_field(name=':x:', value="User undeafened themselves", inline=False)
            if aftervs.self_deaf:
                logembed.add_field(name=':x:', value="User deafened themselves", inline=False)
        elif beforevs.afk != aftervs.afk:
            if beforevs.afk:
                logembed.add_field(name=':x:', value="User left AFK status", inline=False)
            if aftervs.afk:
                logembed.add_field(name=':x:', value="User joined AFK status", inline=False)
        config = self.config_load(member.guild.id)
        logchannel = self.bot.get_channel(int(config['modlogsid']))
        logembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
        await logchannel.send(embed=logembed)

def setup(bot):
    bot.add_cog(logger(bot))