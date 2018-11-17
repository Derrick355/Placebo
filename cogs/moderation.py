import discord
from discord.ext import commands

import time
import asyncio
import json

#########################################################################
# This cog is for moderation related to the bot and guild interaction.  #
# Commands such as ban, kick, settings, and blacklist are found here.   #
#                                                                       #
# There are a total 5 functions made:                                   #
#                                                                       #
#   *config_load - takes a message, returns the config file as a dict   #
#       for the guild the message was sent in.                          #
#   *write_to_config - takes a message and a dict. Stores the dict as   #
#       the guild's config (send the entire config + your edit). The    #
#       guild config is based of the message supplied.                  #
#   *modify_enable_welcome_message - Takes nothing. Flips the value of  #
#        the enablenewmemberchannel boolean in the server's config.     #
#   *modify_welcome_message - Don't use. It's not coded properly. It's  #
#       supposed to modify the welcome message but I havn't figured out #
#       how to change the order of supplied variables for things such   #
#       user's name or guild name.                                      #
#   *modify_enable_leaving_message - Takes nothing. Flips the value of  #
#       enablememberleftmessage boolean in the server's config.         #
#########################################################################


# Gets the config file opened for usage later in a command.
def config_load(m):
    with open(f"data/servers/{m.guild.id}/config.json", 'r', encoding='utf-8') as doc:
        return json.load(doc)

# Mainly for the settings, but this will write to config file for easy editting.
def write_to_config(m, data):
    try:
        with open(f'data/servers/{m.guild.id}/config.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        return True
    except Exception as e:
        return e

class moderation:
    def __init__(self, bot):
        self.bot = bot

    # Purges a set number of messages. If a user if provided at the end, it will go through the number of provided messages and delete any by the provived user.
    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number_to_delete: int, *, params=""):
        """Deletes a set number of messages from the channel. Required permission: manage_messages"""
        try:
            user = ctx.message.mentions[0]
        except:
            pass
        def purgecheck(m):
            if params == "" or user == m.author:
                return True
            else:
                return False
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=number_to_delete, check=purgecheck)
        await ctx.send(f"Deleted {len(deleted)} message(s)", delete_after=5)
    
    # Intial blacklist command to setup the group.
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def blacklist(self, ctx):
        """Add and view words to the blacklist. Required permission: manage_messages"""
        if ctx.invoked_subcommand is None and ctx.message.author.guild_permissions.manage_messages:
            await ctx.send("Please type either `^blacklist add` or `^blacklist listwords`")

    # To add words to the blacklist. Will delete the first message almost immediatly to prevent unwanted words in channels.
    @blacklist.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, *, word_to_ban: str):
        await ctx.message.delete()
        with open(f"data/servers/{ctx.guild.id}/blacklist.txt", "a") as blacklistfile:
            if word_to_ban in blacklistfile:
                ctx.send("That word is already in the blacklist.")
                return
            blacklistfile.write(word_to_ban + "\n")
            await ctx.send(f"Successfully added `{word_to_ban}` to the black list, <@{ctx.message.author.id}>", delete_after=30)
    
    # To list words on the blacklist. List will auto-delete after 30 seconds.
    @blacklist.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def listwords(self, ctx):
        with open(f"data/servers/{ctx.guild.id}/blacklist.txt", "r") as blacklistfile:
            blacklist = blacklistfile.read().splitlines()
        tosend = "Here's a list of all the blacklisted words:"
        num = 1
        for line in blacklist:
            tosend += f"\n{num}. " + line
            num += 1
        await ctx.send(f"{tosend}", delete_after=30)

    # Removes a word. Only will work with a supplied index number based off of the list from the 'listwords' command.
    @blacklist.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def remove(self, ctx, *, index: int):
        index -= 1
        with open(f"data/servers/{ctx.guild.id}/blacklist.txt", "r") as blacklistfile:
            blacklist = blacklistfile.read().splitlines()
            blacklist.pop(index)
        with open(f"data/servers/{ctx.guild.id}/blacklist.txt", "w") as blacklistfile:
            tosend = ''
            for word in blacklist:
                if word != '':
                    tosend += word + '\n'
            blacklistfile.write(tosend)
        await ctx.send("Word Removed.")

    # bans a provided user. By default, number of days to delete messages is set to 1, and reason provided will be None.
    @commands.command()
    #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, name, days_delete_messages: int = 1, *, reason = None):
        """Bans a user from this server. Also deletes previous messages and provides a reason. Required permission: ban_members"""
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.guild.get_member_named(name)
        if not user:
            user = ctx.guild.get_member(int(name))
        if not user:
            user = self.bot.get_user(int(name))
        if not user:
            await ctx.send(':no_entry: Could not find user.')
            return
        if ctx.message.author.top_role > user.top_role:
            banembed = discord.Embed(title=f"You were just banned, {user.name}, from {ctx.message.guild.name}", color=0xff0000)
            banembed.add_field(name="Reason", value="{reason} - Called by {message.author}", inline=True)
            banembed.add_field(name="Time", value="{:%b %d, %Y - %H:%M:%S}".format(ctx.message.created_at), inline=True)
            banembed.set_footer(text="Please do not dm me, I will not respond.")
            await user.send(embed=banembed)
            await ctx.message.guild.ban(user, reason=f"{reason} - Called by {ctx.message.author}", delete_message_days=days_delete_messages)
            await ctx.send(f"{user.name} was successfully banned.")
        else:
            ctx.send(f':no_entry: {ctx.message.author.name}, you must have a higher role than your target.')
    
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, userid):
        fake_member = discord.Object(id=userid)
        await ctx.guild.ban(fake_member)
    
    # Unbans a user. Reason not needed, will say None if none provided.
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userid, *, reason = None):
        """Unbans a user from the server. Required permission: ban_members"""
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.guild.get_member_named(userid)
        if not user:
            user = ctx.guild.get_member(int(userid))
        if not user:
            user = self.bot.get_user(int(userid))
        if not user:
            await ctx.send(':no_entry: Could not find user.')
            return
        try:
            await ctx.message.guild.unban(user, reason="{reason} - Called by {message.author}")
            await ctx.send(f"Successfully unbanned {user.name}")
        except discord.errors.NotFound:
            await ctx.send(":no_entry: They aren't banned")

    # Kicks a user. Reason not required.
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, name, *, reason = None):
        """Kicks a specified user. Required permission: kick_members"""
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.guild.get_member_named(name)
        if not user:
            user = ctx.guild.get_member(int(name))
        if not user:
            user = self.bot.get_user(int(name))
        if not user:
            await ctx.send(':no_entry: Could not find user.')
            return
        if ctx.message.author.top_role > user.top_role or ctx.message.author.id == 186200725276065792:
            kickembed = discord.Embed(title=f"You were just kicked, {user.name}, from {ctx.message.guild.name}", color=0xff0000)
            kickembed.add_field(name="Reason", value=f"{reason} - Called by {ctx.message.author}", inline=True)
            kickembed.add_field(name="Time", value="{:%b %d, %Y - %H:%M:%S}".format(ctx.message.created_at), inline=True)
            kickembed.set_footer(text="Please do not dm me, I will not respond.")
            await user.send(embed=kickembed)
            await ctx.message.guild.kick(user, reason=f"{reason} - Called by {ctx.message.author}")
            await ctx.send(f"{user.name} was successfully kicked.")
        else:
            await ctx.send(f':no_entry: {ctx.message.author.name}, you must have a higher role than your target.')

    # Annouce command (Currently Broken, because it only worked on one server and that server is no longer supported by me.)
    @commands.command(aliases=['announce'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(mention_everyone=True)
    async def announcement(self, ctx, announcement_type: str, *, announcement=""):
        """Starts the proccess of making an announcement Required permission: mention_everyone"""
        if announcement_type.lower() == "normal":
            announcechannel = ctx.guild.get_channel(431296966203277323)
        elif announcement_type.lower() == "staff":
            announcechannel = ctx.guild.get_channel(364543654477692928)
        elif announcement_type.lower() == "freegame":
            announcechannel = ctx.guild.get_channel(449335452894494720)
        else:
            await ctx.send("Sorry, that wasn't a recognized announcement type. Please use normal, staff, or freegame.")
            return
        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author
        if announcement == "":
            try:
                await ctx.send('What is the content of the announcement?')
                announcement = await self.bot.wait_for('message', check=check, timeout=60)
                announcement = announcement.content
            except asyncio.TimeoutError:
                await ctx.send("Canceled.")
                return
            try:
                announceembed = discord.Embed(title='Announcement', description=announcement, color=0x00ff00)
                announceembed.set_footer(text=f"Sent by {ctx.message.author.name}#{ctx.message.author.discriminator}", icon_url=ctx.message.author.avatar_url)
                await ctx.send('Are you sure you want to send this message? (y/n)')
                await ctx.send(embed=announceembed)
                confirmation = await self.bot.wait_for('message', check=check, timeout=10)
            except asyncio.TimeoutError:
                await ctx.send("Canceled.")
                return
            else:
                if confirmation.content.lower() == 'y' or confirmation.content.lower() == 'yes':
                    if announcechannel.id == 431296966203277323 or announcechannel.id == 364543654477692928:
                        await announcechannel.send('@everyone')
                        await announcechannel.send(embed=announceembed)
                    if announcechannel.id == 449335452894494720:
                        freegamerole = discord.utils.get(ctx.guild.roles, name="Free Games")
                        await freegamerole.edit(mentionable=True)
                        await announcechannel.send(freegamerole.mention)
                        await freegamerole.edit(mentionable=False)
                        await announcechannel.send(announcement)
                    return
                else:
                    await ctx.send("Canceled.")
                    return
    
    # Mass DM's every user on the server. Worse than an announcement because it's unblockable if user did not think thourghly.
    @commands.command(aliases=['masspm', 'massdirectmessage', 'massprivatemessage'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def massdm(self, ctx, *, announcement):
        """Mass DMs the server a specified message. Required permission: administrator"""
        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author
        try:
            await ctx.send('Are you sure you want to DM the *entire* server this message? (y/n)')
            massdm = discord.Embed(title='Announcement', description=announcement)
            massdm.set_footer(text=f"Sent by {ctx.message.author.name}#{ctx.message.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            confirmation = await self.bot.wait_for('message', check=check, timeout=10)
        except asyncio.TimeoutError:
            await ctx.send("Canceled.")
            return
        if confirmation.content.lower() == 'y' or confirmation.content.lower() == 'yes':
            for person in ctx.guild.members:
                try:
                    if not person.bot or person != ctx.guild.me:
                        await person.send(embed=massdm)
                except:
                    await ctx.send(f'Missed {person.name}#{person.discriminator}')
            return
        else:
            await ctx.send("Canceled.")
            return

    # Kicks a user from a voice channel. If no user provided, kicks self.
    @commands.command(aliases=['voicekick', 'vckick', 'voicechannelkick'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def vkick(self, ctx, *, name:discord.Member=None):
        if ctx.message.author.id == 186200725276065792:
            await ctx.send('Fuck you.')
            return
        """Kicks user from voice channel. If none specifed, will kick yourself. Required permission: kick_members"""
        if name is None:
            await ctx.send("No user found.")
            return
        else:
            user = ctx.message.author

        if ctx.author.top_role > name.top_role and user.voice is not None:
            vkickchannel = await ctx.guild.create_voice_channel(f'vkick-{name.display_name}')
            await name.move_to(vkickchannel)
            await vkickchannel.delete()
            await ctx.send(f":white_check_mark: {ctx.author.display_name}, {name.display_name} was voice kicked from {name.voice.channel.name}")
        elif user.voice is None:
            if ctx.author != name:
                await ctx.send(f":no_entry: {ctx.author.name}, that person isn't connected to a voice channel right now.")
            if ctx.author == name:
                await ctx.send(f":no_entry: {ctx.author.name}, you aren't connected to a voice channel right now.")
        elif ctx.author.top_role <= user.top_role:
            await ctx.send(f":no_entry: {ctx.author.name}, you need to have a higher role than your target.")

    # I forgot what this does cause it doesn't fucking work.
    async def on_error(self, error, ctx):
        await ctx.send(error)

    # Function for modify the location of mod logs, because it is used in 2 different commands.
    async def modify_mod_logs(self, ctx):
        def authorcheck(m):
            if m.author == ctx.message.author:
                return True
        await ctx.send('Please say the **Channel ID** *(This should be a number)* of which you would like to change the Mod Logs channel to, or type "cancel" to cancel.')
        try:
            new_channel_id_message = await self.bot.wait_for('message', check=authorcheck, timeout=20)
        except asyncio.TimeoutError:
            await ctx.send('Nothing recieved. Canceling.')
            return 'cancel'
        if new_channel_id_message.content.lower() == 'cancel':
            await ctx.send('Canceled.')
            return 'cancel'
        try:
            new_channel_id = int(new_channel_id_message.content)
        except:
            await ctx.send('That doesn\'t look like a number to me. Please retry the command.')
            return 'cancel'
        testing = ctx.message.guild.get_channel(new_channel_id)
        if testing is None or not isinstance(testing, discord.TextChannel):
            await ctx.send('That doesn\'t look like a text channel to me. Please retry the command.')
            return 'cancel'
        config = config_load(ctx.message)
        config['modlogsid'] = new_channel_id
        result = write_to_config(ctx.message, config)
        if result != True:
            await ctx.send(f'Error.\n{result}')
        elif result:
            await ctx.send('Changed!')
    
    # Function for enabling/disabling the welcome message, because it is used in 2 different commands.
    async def modify_enable_welcome_message(self, ctx):
        def authorcheck(m):
            if m.author == ctx.message.author:
                return True
        config = config_load(ctx.message)
        if config['enablenewmemberchannel']:
            await ctx.send('The welcome message is currently enabled. Would you like to disable it?')
            try:
                confirmation = await self.bot.wait_for('message', check=authorcheck, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send('Nothing recieved. Canceling.')
                return 'cancel'
            if 'y' in confirmation.content.lower() or 'yes' in confirmation.content.lower():
                config['enablenewmemberchannel'] = False
                result = write_to_config(ctx.message, config)
                if result != True:
                    await ctx.send(f'Error.\n{result}')
                elif result:
                    await ctx.send('Changed!')
            else:
                await ctx.send('Canceled.')
                return 'cancel'
        if not config['enablenewmemberchannel']:
            await ctx.send('The welcome message is currently disabled. Would you like to enable it?')
            try:
                confirmation = await self.bot.wait_for('message', check=authorcheck, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send('Nothing recieved. Canceling.')
                return 'cancel'
            if 'y' in confirmation.content.lower() or 'yes' in confirmation.content.lower():
                config['enablenewmemberchannel'] = True
                result = write_to_config(ctx.message, config)
                if result != True:
                    await ctx.send(f'Error.\n{result}')
                elif result:
                    await ctx.send('Changed!')
            else:
                await ctx.send('Canceled.')
                return 'cancel'
    
    # Function for modifing the welcome message, but beacause I suck at coding, DON'T USe THIS.
    async def modify_welcome_message(self, ctx):
        def authorcheck(m):
            if m.author == ctx.message.author:
                return True
        config = config_load(ctx.message)
        if not config['enablenewmemberchannel']:
            ctx.send('You need to enable welcome messages to modify this setting.')
            return 'cancel'
        try:
            await ctx.send(f"What would you like to change your welcome message to? Type \"cancel\" to cancel.\nIt is currently set to:\n {config['newmembermessage']}")
            await ctx.send('Here are the availble variables: {guild.name\\} and {member.id\\}')
            new_message = await self.bot.wait_for('message', check=authorcheck, timeout=20)
        except asyncio.TimeoutError:
            await ctx.send('Nothing recieved. Canceling.')
            return 'cancel'
        if 'cancel' in new_message.content:
            await ctx.send('Canceled')
            return 'cancel'
        config['newmembermessage'] = new_message.content
        result = write_to_config(ctx.message, config)
        if result != True:
            await ctx.send(f'Error.\n{result}')
        elif result:
            await ctx.send('Changed!')

    # Enable/disable leaving message in the welcome channel set in an earlier function.
    async def modify_enable_leaving_message(self, ctx):
        def authorcheck(m):
            if m.author == ctx.message.author:
                return True
        config = config_load(ctx.message)
        if config['enablememberleftmessage']:
            await ctx.send('The leaving message is currently enabled. Would you like to disable it?')
            try:
                confirmation = await self.bot.wait_for('message', check=authorcheck, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send('Nothing recieved. Canceling.')
                return 'cancel'
            if 'y' in confirmation.content.lower() or 'yes' in confirmation.content.lower():
                config['enablememberleftmessage'] = False
                result = write_to_config(ctx.message, config)
                if result != True:
                    await ctx.send(f'Error.\n{result}')
                elif result:
                    await ctx.send('Changed!')
            else:
                await ctx.send('Canceled.')
                return 'cancel'
        if not config['enablememberleftmessage']:
            await ctx.send('The leaving message is currently disabled. Would you like to enable it?')
            try:
                confirmation = await self.bot.wait_for('message', check=authorcheck, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send('Nothing recieved. Canceling.')
                return 'cancel'
            if 'y' in confirmation.content.lower() or 'yes' in confirmation.content.lower():
                config['enablememberleftmessage'] = True
                result = write_to_config(ctx.message, config)
                if result != True:
                    await ctx.send(f'Error.\n{result}')
                elif result:
                    await ctx.send('Changed!')
            else:
                await ctx.send('Canceled.')
                return 'cancel'

    # Main group for settings. From here it will activate the other set functions as needed.
    @commands.group(invoke_without_command=True, aliases=['setting', 'configure', 'config'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def settings(self, ctx):
        gottem = False
        def authorcheck(m):
            if m.author == ctx.message.author:
                return True
        await ctx.send('Availble settings to modify:\n1. Mod Logs Channel\n2. Enable/Disable Welcome Message\n3. Enable/Disable Leaving Message')
        while not gottem:
            try:
                settings_choice = await self.bot.wait_for('message', check=authorcheck, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send('Nothing recieved. Canceling.')
                return
            if '1' in settings_choice.content or 'mod logs channel' in settings_choice.content.lower():
                gottem = True
                result = await self.modify_mod_logs(ctx)
                if result == 'cancel':
                    return
            elif '2' in settings_choice.content or 'enable/disable welcome message' in settings_choice.content.lower():
                gottem = True
                result = await self.modify_enable_welcome_message(ctx)
                if result == 'cancel':
                    return
            # This next part was commented out because i suck at coding, and I don't know how to make it work the way I want it to, well.
            #elif '3' in settings_choice.content or 'change welcome message' in settings_choice.content.lower():
            #    gottem = True
            #    result = await self.modify_welcome_message(ctx)
            #    if result == 'cancel':
            #        return
            elif '3' in settings_choice.content or 'enable/disable welcome message' in settings_choice.content.lower():
                gottem = True
                result = await self.modify_enable_leaving_message(ctx)
                if result == 'cancel':
                    return
            else:
                await ctx.send('Invalid choice.')
                gottem = False

    # Subgroup command for calling the modify mod logs channel function.
    @settings.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def mod_logs_channel(self, ctx):
        result = await self.modify_mod_logs(ctx)
        if result == 'cancel':
            return
    
    # Subgroup command for calling the enable welcome message function
    @settings.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def enable_welcome_message(self, ctx):
        result = await self.modify_enable_welcome_message(ctx)
        if result == 'cancel':
            return
    
    # Again, I suck at coding.
    #@settings.command()
    #async def change_welcome_message(self, ctx):
    #    if not ctx.message.author.guild_permissions.manage_guild:
    #        await ctx.send(':no-entry: You don\'t have permission to modify bot settings')
    #        return
    #    result = await self.modify_welcome_message(ctx)
    #    if result == 'cancel':
    #        return

    # Subgroup command for calling the enable leaving message function.
    @settings.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def enable_leaving_message(self, ctx):
        result = await self.modify_enable_leaving_message(ctx)
        if result == 'cancel':
            return

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def lockdown(self, ctx):
        config = config_load(ctx.message)
        if not config['lockdownmode']:
            config['lockdownmode'] = True
            write_to_config(ctx.message, config)
            await ctx.send('Lockdown enabled.')
            return
        elif config['lockdownmode']:
            config['lockdownmode'] = False
            write_to_config(ctx.message, config)
            await ctx.send('Lockdown disabled.')
            return

def setup(bot):
    bot.add_cog(moderation(bot))