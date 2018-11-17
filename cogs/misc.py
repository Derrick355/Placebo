import discord
from discord.ext import commands

import os
import sys
import time
import json
import datetime
import asyncio
import aiohttp
import urllib.request
import urllib.parse
import urllib.error

#########################################################################
# Misc. commands such as ping and help can be found here.               #
#########################################################################

# Gets the config file opened for usage later in a command.
def guild_config_load(gid):
    with open(f"data/servers/{gid}/config.json", 'r', encoding='utf-8') as doc:
        return json.load(doc)

def config_load():
    with open('data/config.json', 'r', encoding='utf-8') as doc:
        #  Please make sure encoding is correct, especially after editing the config file
        return json.load(doc)

class misc:
    def __init__(self, bot):
        self.bot = bot

    # Add suggestions for the bot. Currently broken as the server it sends the messages to is no longer supported and I have yet to fix it.
    @commands.command(aliases=['suggestion'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion: str):
        if ctx.author.id == 263883999687081984:
            return
        """Use this to suggest a feature to add to the bot or server"""
        suggestionchannel = ctx.guild.get_channel(477198256737353729) # Gets needed channel
        suggestionembed = discord.Embed(title=f"{ctx.message.author.name}#{ctx.message.author.discriminator} made a suggestion", description=suggestion, color = 0x0000ff) # creates the embed
        suggestionembed.set_footer(text="{:%b %d, %Y - %H:%M:%S}".format(datetime.datetime.now()))
        await suggestionchannel.send(embed=suggestionembed) # Records the suggestion
        await ctx.send("Thanks! I've recorded your suggestion.") # Confirmation for the user that it was sent.
    
    # Gets current delay from bot to server.
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):
        """Gets the current delay from you to the bot"""
        global starttime 
        starttime = time.time() # Starts the timer
        await ctx.send("Pong!") # Sends message
    
    # See above.
    async def on_message(self, message):
        if message.author.id == 500165490753404938 and message.content == "Pong!": # Checks to make sure that for the message sent is for the Pong command.
            endtime = time.time() # captures end time
            difference = 1000 * (float(endtime) - float(starttime)) # figures out time difference
            difference = int(difference)
            await message.edit(content=f"Pong! - Took {difference}ms") # Modifies message with response time

    # new help command I made to replace the old, weird looking one that didn't work with permissions. Uses embeds and sends it via DM's
    # Also, moderation commands will only show if they have the right permissions for the server the help command was run in.
    @commands.command(aliases=['commands'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def help(self, ctx):
        """Shows this message."""
        modstatus=False
        helpembed = discord.Embed(title="Commands", description=f"Commands everyone has access to.\nServer Prefix: {ctx.prefix}", color=0x631093) # Starts the creation of the help embed.
        helpembed.add_field(name="chucknorris", value="Returns a 100% true fact about Chuck Norris", inline=False)
        helpembed.add_field(name="eightball [question]", value="Ask the majic 8 ball any question, and you may recieve an answer", inline=False)
        #helpembed.add_field(name="lfg", value="Toggles your LFG status", inline=False)
        helpembed.add_field(name="numberfact [number]", value="Input a number and recieve a fact based on that number.", inline=False)
        helpembed.add_field(name="rockpaperscissors [rock, paper, or scissors]", value="Play rock paper scissors with the bot.", inline=False)
        helpembed.add_field(name="ronswanson", value="Returns a quote from Ron Swanson.", inline=False)
        helpembed.add_field(name="ping", value="Returns the current bot ping.", inline=False)
        helpembed.add_field(name="suggest [suggestion]", value="Suggest a feature for the bot or server", inline=False)
        helpembed.add_field(name="hangman", value="Play hangman!", inline=False)
        helpembed.add_field(name="numberfact", value="Get a fact about a number!", inline=False)
        helpembed.add_field(name="oof", value="OOF", inline=False)
        helpembed.add_field(name="version", value="Returns the current version of the bot", inline=False)
        helpembed.add_field(name="bobross", value="Prints a quote from famed artist Bob Ross", inline=False)
        #helpembed.add_field(name='face [image_url] <args>', value='Get some information on a provided face. Only .jpg Filetypes. \nAcceptable Args: --age --gender --glasses --facialHair --emotion --hair --makeup\nExample:\n[p]face https://www.pcgamesn.com/wp-content/uploads/2018/10/gabe_newell_meme-580x334.jpg --age --gender --makeup')
        helpembed.add_field(name='die <number>', value='Rolls a die. If no number specifed, will roll a 6-sided die.')
        helpembed.add_field(name='lovecalc [name] <name2>', value='Calculates the chances of 2 people to fall in love. If name2 isn\'t provided, it will assume the message author.')
        helpembed.add_field(name='mathquiz', value='Take a quiz! Either add or subtract two numbers ranging from -99 to +99.')
        helpembed.add_field(name='Music', value=f'To see commands related to music, type {ctx.prefix}helpmusic')
        await ctx.author.send(embed=helpembed)
        modembed = discord.Embed(title="Moderator Commands", descripton="Commands only certain staff have access to", color=0x000000) # This will only show up if the user in question has access to any of the commands below.
        if ctx.message.author.guild_permissions.manage_messages:
            modembed.add_field(name="purge [number to delete]", value="Deletes a set number of messages", inline=False)
            modembed.add_field(name="blacklist [add [word] / listwords]", value="Add a word or list all words on the blacklist", inline=False)
            modstatus=True
        if ctx.message.author.guild_permissions.ban_members:
            modembed.add_field(name="ban [user] [how many messages to delete in days] [reason]", value="Bans a user from the server.", inline=False)
            modembed.add_field(name="unban [user id] <reason>", value="Unbans a user from the server.", inline=False)
            modstatus=True
        if ctx.message.author.guild_permissions.kick_members:
            modembed.add_field(name="kick [user] <reason>", value="Kicks a user from the server", inline=False)
            modembed.add_field(name="vkick <user>", value="Kicks a user form their current voice channel. If no user specifed, kicks yourself.", inline=False)
            modstatus=True
        if ctx.message.author.guild_permissions.mention_everyone and ctx.message.guild.id == 275833983856803840:
            modembed.add_field(name="announcement [type] <content>", value="Simple announcement. Availble types are: normal, freegame, staff", inline=False)
            modstatus=True
        if ctx.message.author.guild_permissions.administrator:
            modembed.add_field(name="massdm [announcement]", value="Sends a DM to every user on the server.", inline=False)
            modstatus=True
        appinfo = await self.bot.application_info()
        if appinfo.owner == ctx.message.author:
            modembed.add_field(name="say [message]", value="Bot will delete your message then repeat what you told it to", inline=False)
            modstatus=True
        if modstatus: # Makes sure that it will only send if the user has permission.
            await ctx.author.send(embed=modembed)
    
    @commands.command(aliases=['musichelp', 'helpm', 'mhelp'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def helpmusic(self, ctx):
        mhelpembed = discord.Embed(title='Music Commands', description='Play music!', color = 0xe00ae6) #Prepares the help command for the music cog
        mhelpembed.add_field(name="play [link/search]", value='Play a song. Accepts YT links and searches.', inline=False)
        mhelpembed.add_field(name='pause', value='Pauses current song', inline=False)
        mhelpembed.add_field(name='resume', value='Resumes current song', inline=False)
        mhelpembed.add_field(name='stop', value='Stops the player', inline=False)
        mhelpembed.add_field(name='connect <channel>', value='Joins provivded voice channel. If none provided, will attempt to join yours.', inline=False)
        mhelpembed.add_field(name='skip', value='Skips the current song.', inline=False)
        mhelpembed.add_field(name='queue_info', value='Retrieve a baisc queue of upcoming songs.', inline=False)
        mhelpembed.add_field(name='now_playing', value='Displays information about the currently playing song.', inline=False)
        mhelpembed.add_field(name='change_volume', value='Change the player\'s volume', inline=False)
        await ctx.author.send(embed=mhelpembed) # Sends it via DM's

    @commands.command(aliases=["v", "ver"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def version(self, ctx):
        config = config_load()
        python_version = sys.version_info
        await ctx.send(f"Bot Version {config['version']}\nDiscord.py Version {discord.__version__}\nPython Version {python_version[0]}.{python_version[1]}.{python_version[2]}")

    # Orignally used for telling if two certain people are streaming, but one rage quitted on streaming and the other was arrested for 17 different
    # accounts of assult and possesion of a deadly weapon towards his girlfriend at the time.
    # Don't worry the girlfriend is fine.
    #async def on_member_update(self, mbefore, mafter):
    #    if mbefore.activity != mafter.activity and isinstance(mafter.activity, discord.Streaming) and "twitch.tv" in mafter.activity.url:
    #        if mafter.id == 203390693022892032 or mafter.id == 462417171105054730:
    #            twitchchannel = mafter.guild.get_channel(464681092319019008)
    #            await twitchchannel.send(f'{mafter.name} just started streaming!\n{mafter.activity.url}')

    @commands.command(aliases=["chars", "char", "character"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def characters(self, ctx, *, word):
        await ctx.send(f"It's {len(word)} characters")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def license(self, ctx):
        print("test")
        with open(f"license.txt", 'r', encoding='utf-8') as doc:
            print("test2")
            my_str = doc.read()
            print(my_str)
            new_str = my_str.replace("Mihanovich", "**********")
            print(new_str)
            await ctx.send(f"```{new_str}```", delete_after=60)

    # @commands.command(aliases=['qrcode', 'qr_code'])
    # @commands.cooldown(1, 10, commands.BucketType.user)
    # async def qr(self, ctx, link):
    #     print('huh1')
    #     async with ctx.channel.typing():
    #         print('huh2')
    #         async with aiohttp.ClientSession() as session:
    #             print('huh3')
    #             link = urllib.parse.quote(link)
    #             print('huh4')
    #             params={"data": link,
    #                 "size": "150x150"}
    #             async with session.get(f'https://api.qrserver.com/v1/create-qr-code', params=params) as resp: # Sends the URL
    #                 print('huh5')

    @commands.command()
    async def qr(self, ctx, *,message): 
        message = urllib.parse.quote(message)
        e = discord.Embed(title=message, color=0x000000)
        e.set_image(url = f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=\"{message}\"')
        await ctx.send(embed = e)


def setup(bot):
    bot.add_cog(misc(bot))