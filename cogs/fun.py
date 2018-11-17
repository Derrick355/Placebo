import discord
from discord.ext import commands

import json
import http.client
import random
import time
import random
import asyncio
import aiohttp
import urllib.request
import urllib.parse
import urllib.error
import os

#########################################################################
# Cog for entertainment related commands such as 8ball, ronswanson, and #
# rockpaperscissors can be found here.                                  #
#                                                                       #
# Only 1 function is made here:                                         #
#   *randomWord - Takes nothing. Returns a word from a list of over 300 #
#       thousand words.                                                 #
#########################################################################

# For getting a random word. It's set like this for future reference, but if i'm correct (too lazy to check) it's only used once right now.
# The random word is from a .json list of over 370k words.
def randomWord():
    with open('data/words.json') as f:
        data = json.load(f)
        #print(len(data))
    data = list(data.keys())
    word = data[random.randint(1, 370102)]
    #print(word)
    return word.lower()

def load_user_config(ctx):
    with open(f'data/servers/{ctx.guild.id}/users.json', "r", encoding="utf-8") as doc:
        user_config = json.load(doc)
        try:
            user_config2 = user_config['users'][str(ctx.author.id)]
            if user_config2 is not None:
                pass
            return user_config
        except KeyError:
            with open(f'data/servers/{ctx.guild.id}/users.json', "w", encoding="utf-8") as doc:
                user_config['users'][str(ctx.author.id)] = user_config['default']
                json.dump(user_config, doc, indent=4)
                return user_config

def write_to_user_config(ctx, data):
    with open(f'data/servers/{ctx.guild.id}/users.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

class fun:
    def __init__(self, bot):
        self.bot = bot

    # Simple 8ball command. A question must be asked, which ends with a question mark, and it also uses an API to recieve answers.
    # I seriously could've done this without an API, but it's my first API that I used so fuck you.
    @commands.command(aliases=['8ball', '8'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def eightball(self, ctx, *, question):
        """Ask the magic 8 ball any question, and you may recieve an answer"""
        await ctx.message.channel.trigger_typing() # Triggers the Placebo is typing
        if question.endswith('?'): # Makes sure that the question is a question
            async with aiohttp.ClientSession() as session: # Opens a session
                question = urllib.parse.quote(question) # Makes the question into a format readable in a URL, by doing things such as replacing " " with "%20"
                async with session.get(f'http://8ball.delegator.com/magic/JSON/{question}') as resp: # Sends the URL
                    #print(resp.status)
                    #print(await resp.text())
        #    conn = http.client.HTTPSConnection("8ball.delegator.com")
        #    question = urllib.parse.quote(question)
        #    conn.request('GET', '/magic/JSON/' + question)
        #    response = conn.getresponse()
                    resp = json.loads(await resp.read()) # Takes the response about interprets it into a variable. Usually a list or dictionary.
                    resp = resp['magic'] # Takes the 'magic' part of the provided dictionary (because it's the only one so idk why they even bothered with that. Maybe future compatibility?)
                    if resp['type'] == 'Affirmative': # Adds a check mark if response type is affirm
                        emoji = ':white_check_mark: '
                    elif resp['type'] == 'Contrary': # Adds a red X if the response is negative
                        emoji = ':x: '
                    elif resp['type'] == 'Neutral': # Adds a grey question mark if response type is unknown
                        emoji = ':grey_question: '
                    await ctx.send(':8ball: ' + emoji + resp['answer']) # Sends the message.
        else:
            await ctx.send("That doesn't look like a question.")
        
    # Play rock paper scissors. Bot's choice is dependant on a random number generator.
    @commands.command(aliases=['rps', 'roshambo', 'rso'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def rockpaperscissors(self, ctx, choice):
        """Play rock paper scissors with the bot! Choose from rock, paper, or scissors"""
        await ctx.message.channel.trigger_typing() # Triggers typing
        random_choice = random.randint(1,3) # Gets a random INT as the bot's choice.
        if (choice.lower() == "r") or (choice.lower() == "rock"): # Starts the win/lose check. This line is if the user chose "rock"
            if random_choice == 1: # If the bot chose rock
                await ctx.send("I play... :moyai:\nWell then, we tied.")
            if random_choice == 2: # If the bot chose paper
                await ctx.send("I play... :page_facing_up:!\nYay, I win!")
            if random_choice == 3: # if the bot chose scissors
                await ctx.send("I play... :scissors:!\nAww, I lost!")
        if (choice.lower() == "p") or (choice.lower() == "paper"): # If the user chose "paper"
            if random_choice == 1: # if the bot chose rock
                await ctx.send("I play... :moyai:!\nAww, I lost!")
            if random_choice == 2: # if the bot chose paper
                await ctx.send("I play... :page_facing_up:!\nWell then, we tied.")
            if random_choice == 3: # if the bot chose scissors
                await ctx.send("I play... :scissors:!\nYay, I win!")
        if (choice.lower() == "s") or (choice.lower() == "scissors"): # if the user chose "scissors"
            if random_choice == 1: # if the bot chose rock
                await ctx.send("I play... :moyai:!\nYay, I win!")
            if random_choice == 2: # if the bot chose paper
                await ctx.send("I play... :page_facing_up:!\nAww, I lost!")
            if random_choice == 3: # if the bot chose scissors
                await ctx.send("I play... scissors:!\nWell then, we tied.")
    
    # Toggles LFG status for a server no longer in use, so this is also broken af.
    # Well, actually, this can work as long as the server in question has a role called LFG.
    @commands.command(aliases=['lookingforgroup'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lfg(self, ctx):
        try: # checks if the server has a role called LFG.
            lfg_role = discord.utils.get(ctx.guild.roles, name="LFG")
            supported = True
        except AttributeError: # If not, tells user it's unsupported.
            await ctx.send(f'This server doesn\'t support the Looking for Group features. Ask {ctx.message.guild.owner.display_name} to enable it!')
            supported = False
            return
        if not "lfg" in [y.name.lower() for y in ctx.message.author.roles] and supported: # If they don't have the role, it will add it to them.
            await ctx.message.author.add_roles(lfg_role)
            await ctx.send(f"<@{ctx.message.author.id}>, you have been marked as Looking For Group (LFG)")
        elif "lfg" in [y.name.lower() for y in ctx.message.author.roles] and supported: # If they already have the role, will remove it from them.
            await ctx.message.author.remove_roles(lfg_role)
            await ctx.send(f"<@{ctx.message.author.id}>, you have been marked as no longer Looking For Group (LFG)")

    # Returns a fact about Chuck Norris.
    @commands.command(aliases=['chuck', 'norris'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def chucknorris(self, ctx):
        """Returns a 100% true fact about Chuck Norris"""
        await ctx.message.channel.trigger_typing() # triggers typing
        async with aiohttp.ClientSession() as session: # Opens session
            async with session.get(f'https://api.chucknorris.io/jokes/random') as resp: # gets response
                #print(resp.status)
                #print(await resp.text())
        #response = requests.get("https://api.chucknorris.io/jokes/random")
                data = await resp.json() # interprets response
                await ctx.send(data["value"]) # prints response
    
    # Returns a quote from the ever-famous Ron Swan from the TV show Parks and Rec.
    @commands.command(aliases=['ron', 'swanson'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ronswanson(self, ctx):
        """Returns a quote by Ron Swanson, a character in the TV Show Parks & Rec"""
        await ctx.message.channel.trigger_typing()# triggers typing
        async with aiohttp.ClientSession() as session: # opens session
            async with session.get(f'http://ron-swanson-quotes.herokuapp.com/v2/quotes') as resp: # gets response
                #print(resp.status)
                #print(await resp.text())
        #response = requests.get("http://ron-swanson-quotes.herokuapp.com/v2/quotes")
                if resp.status == 200:
                    data = await resp.json() # interperts data recieved
                    #print(resp)
                    #print(data)
                    await ctx.send(f'"{data[0]}" - Ron Swanson') # prints data recieved

    # OOF
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def oof(self, ctx):
        """OOF"""
        await ctx.send(file=discord.File(open('data/OOF.mp3','rb'), filename="OOF.mp3")) # sends the OOF.mp3 found in /data/
    
    # Returns a fact about a given number.
    @commands.command(aliases=['num', 'number'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def numberfact(self, ctx, number: int):
        await ctx.message.channel.trigger_typing() # trigger typing
        async with aiohttp.ClientSession() as session: # opens session
            async with session.get(f'http://numbersapi.com/{number}') as resp: # gets response
                #print(resp.status)
                #print(await resp.text())
        #response = requests.get(f"http://numbersapi.com/{number}")
                await ctx.send(str(await resp.text())) # sends response

    # NO U
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def biggay(self, ctx):
        await ctx.send("no u") # NO U
    
    # Play a game of hangman. Anyone can participate, and the person who intially ran the command can either provice their own word, or the bot can provide a 
    # word using the random word function mentioned earlier.
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hangman(self, ctx):
        # For delcaring variables used later
        got_word = False # Used for the while loop while trying to get the word from a user if they chose custom word.
        guesses = ""
        blank_spaces = ""
        def authorcheck(m): # For a wait_for, checks if the message it cause is by the same author.
            if m.author == ctx.message.author and m.author != ctx.guild.me:
                return True
        def charcheck(m): # Also for the wait_for, checks if the message it caught was in the same channel as the original message.
            if m.channel == ctx.message.channel and len(m.content) == 1 and m.author != ctx.guild.me:
                return True
        await ctx.send("Lets play hangman! Do you want to use a randomly generated word (type random) or do you want to make one (type custom)?")
        try: # Asks how they want the word to be selected.
            firstconfirm = await self.bot.wait_for('message', check=authorcheck, timeout=20) # Waits for a message for how the user wants the message to be selected. If user waits too long, raises a timeout error.
        except asyncio.TimeoutError: # If they wait too long (20 seconds), it will raise 'asyncio.TimeoutError' and this will cancel the entire command.
            await ctx.send('Message not recieved in time. Canceling.')
            return
        if firstconfirm.content.lower() == "random": # if it's random they choose, will use the predefined function to get a word.
            word = str(randomWord())
        elif firstconfirm.content.lower() == "custom": # else, it will activate this cancer.
            try:
                await ctx.author.send('Hey! What word do you want to use?') # Asks question
                await ctx.send('I just sent you a message.') # Tells user a message was sent via DM's
                while not got_word: # Wile the bot has yet to get the word,
                    word = await self.bot.wait_for('message', check=authorcheck, timeout=20) # it will look for a message by the author
                    if " " in word.content: # if the message contains a space it will not work
                        await ctx.message.author.send('Sorry, no spaces! Please try again.')
                    else:
                        word = word.content.lower() # puts the word in lowercase and sets it for the game.
                        got_word = True # ends the while loop.
            except asyncio.TimeoutError: # if no message was caught in time (20 seconds)
                await ctx.send('Message not recieved in time. Canceling.')
                return
            except Exception as e: # If there is some sort of error this will catch and print it.
                error = f'{type(e).__name__} : {e}'
                await ctx.send(f'I had an error:\n {error}')
        turns = round((len(word) / 2) + len(word)) # Figures out how many turns users should get base of the length of the word. It's about 1.5x the length of the word, rounded up.
        while turns > 0: # Loops while users still have turns left.
            failed = 0
            blank_spaces = ''
            for char in word: # for every character in word
                if char in guesses: # if the character has been succesfully guessed, it will add it to the blank_spaces variable to print what has been found later.
                    blank_spaces = blank_spaces + char + ' '
                else: # else, it will print and underscore.
                    blank_spaces += "_ "
                    failed += 1 # and add one to failed characters
            await ctx.send(f'`{blank_spaces}`') # sends the blank spaces
            if failed == 0: # if failed is zero, it means every character has been guessed and the users have won.
                await ctx.send('You won!')
                return
            await ctx.send('Guess a character') # otherwise, it will as for a character
            try: # again, waits for a response in the same channel
                character = await self.bot.wait_for('message', check=charcheck, timeout=60)
            except asyncio.TimeoutError: # if no one plays within 1 minute, game ends.
                ctx.send('No one has played in the past 1 minute. Canceling now.')
                return
            guesses += character.content.lower() # puts the letter said into guesses as lowercase to later check. See above.
            if character.content.lower() not in word: # If the letter guessed isn't in the word, removes one from turns.
                turns -= 1
                await ctx.send(f'Wrong! You have {turns} more guesses left.') # Announces that it is wrong and dispalys how many turns are left.
                if turns == 0: # if no turns are left, ends the game.
                    await ctx.send(f'You lose! The word was {word}')
                    return

    # Dad jokes part. If any message begins with im, i'm or i am (in any case), it will say what they put in the style of a dad joke, while also changing their
    # nick name if the bot has permission.
    async def on_message(self, message):
        im_dad_thingy = ""
        send = False
        to_test = message.content.lower() # converts message to lowercase for testing if it's valid for a dad joke.
        if to_test.startswith('im '):
            im_dad_thingy = message.content[3:] # takes the 'im' part out
            send = True # says that it's a proper setup
        elif to_test.startswith("i'm "):
            im_dad_thingy = message.content[4:] # see above
            send= True # see above
        elif to_test.startswith("i am "):
            im_dad_thingy = message.content[5:] # see above
            send = True # see above
        if message.author.bot:
            send = False
        if send: # if it's a proper setup
            await message.channel.send(f"Hey {im_dad_thingy}! I'm {message.guild.me.display_name}") # it will send a message
            try: # it will try to change his name
                await message.author.edit(reason="Dad Jokes", nick=im_dad_thingy)
            except discord.Forbidden: # and if it can't, just does nothing.
                pass
            except discord.HTTPException:
                pass

    # Probably the most complicated use of an API I've ever done to this point (10/15/2018) because it actually sends an image also!
    # If certain attributes are provided, will send information about those.
    # Commenting out because I really don't feel like updating it to use AIOHTTP instead of REQUESTS
    """
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def face(self, ctx, image_url, *, parameters=''):
        subscription_key = "f6da36ee8ced4f569686b53922892cbb"
        assert subscription_key

        face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'

        #image_url = 'https://how-old.net/Images/faces2/main007.jpg'

        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,smile,facialHair,glasses,' +
            'emotion,hair,makeup,accessories'
        }
        data = {'url': image_url}
        response = requests.post(face_api_url, params=params, headers=headers, json=data)
        faces = response.json()
        print(faces)
        to_send = "Here's your data!\n"
        if '--age' in parameters:
            to_send = to_send + "Age: " + str(faces[0]['faceAttributes']['age']) + '\n'
        if '--gender' in parameters:
            to_send = to_send + 'Gender: ' + str(faces[0]['faceAttributes']['gender']) + '\n'
        if '--glasses' in parameters:
            to_send = to_send + 'Glasses: ' + str(faces[0]['faceAttributes']['glasses']) + '\n'
        if '--facialHair' in parameters:
            to_send = to_send + 'Moustache: ' + str(faces[0]['faceAttributes']['facialHair']['moustache']) + '\n'
            to_send = to_send + 'Beard: ' + str(faces[0]['faceAttributes']['facialHair']['beard']) + '\n'
            to_send = to_send + 'Sideburns: ' + str(faces[0]['faceAttributes']['facialHair']['sideburns']) + '\n'
        if '--emotion' in parameters:
            to_send = to_send + 'Anger: ' + str(faces[0]['faceAttributes']['emotion']['anger']) + '\n'
            to_send = to_send + 'Contempt: ' + str(faces[0]['faceAttributes']['emotion']['contempt']) + '\n'
            to_send = to_send + 'Disgust: ' + str(faces[0]['faceAttributes']['emotion']['disgust']) + '\n'
            to_send = to_send + 'Fear: ' + str(faces[0]['faceAttributes']['emotion']['fear']) + '\n'
            to_send = to_send + 'Happiness: ' + str(faces[0]['faceAttributes']['emotion']['happiness']) + '\n'
            to_send = to_send + 'Neutral: ' + str(faces[0]['faceAttributes']['emotion']['neutral']) + '\n'
            to_send = to_send + 'Sadness: ' + str(faces[0]['faceAttributes']['emotion']['sadness']) + '\n'
            to_send = to_send + 'Surprise: ' + str(faces[0]['faceAttributes']['emotion']['surprise']) + '\n'
        if '--hair' in parameters:
            to_send = to_send + 'Bald: ' + str(faces[0]['faceAttributes']['hair']['bald']) + '\n'
            to_send = to_send + 'Invisible: ' + str(faces[0]['faceAttributes']['hair']['invisible']) + '\n'
            to_send = to_send + str(faces[0]['faceAttributes']['hair']['hairColor'][0]['color']) + ': ' + str(faces[0]['faceAttributes']['hair']['hairColor'][0]['confidence']) + '\n'
            to_send = to_send + str(faces[0]['faceAttributes']['hair']['hairColor'][1]['color']) + ': ' + str(faces[0]['faceAttributes']['hair']['hairColor'][1]['confidence']) + '\n'
            to_send = to_send + str(faces[0]['faceAttributes']['hair']['hairColor'][2]['color']) + ': ' + str(faces[0]['faceAttributes']['hair']['hairColor'][2]['confidence']) + '\n'
            to_send = to_send + str(faces[0]['faceAttributes']['hair']['hairColor'][3]['color']) + ': ' + str(faces[0]['faceAttributes']['hair']['hairColor'][3]['confidence']) + '\n'
            to_send = to_send + str(faces[0]['faceAttributes']['hair']['hairColor'][4]['color']) + ': ' + str(faces[0]['faceAttributes']['hair']['hairColor'][4]['confidence']) + '\n'
            to_send = to_send + str(faces[0]['faceAttributes']['hair']['hairColor'][5]['color']) + ': ' + str(faces[0]['faceAttributes']['hair']['hairColor'][5]['confidence']) + '\n'
        if '--makeup' in parameters:
            to_send = to_send + 'Eye Makeup: ' + str(faces[0]['faceAttributes']['makeup']['eyeMakeup']) + '\n'
            to_send = to_send + 'Lip Makeup: ' + str(faces[0]['faceAttributes']['makeup']['lipMakeup']) + '\n'
        await ctx.send(to_send)
    """

    # A command to roll a die. If no number provided, will roll a 6 sided die.
    @commands.command(aliases=['dice'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def die(self, ctx, sides=6):
        await ctx.send('The die rolls {}'.format(random.randint(1, sides))) # roles a dice.

    @commands.command(aliases=['bob', 'ross'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bobross(self, ctx):
        await ctx.message.channel.trigger_typing()# triggers typing
        with open('data/bobrossquotes.json') as f: # with the file full of bob ross quotes open,
            data = json.load(f) # takes the file and converts it to a list
            #print(len(data))
            quote = data[random.randint(1, len(data))] # chooses a random quote
            await ctx.send(f'"{quote}" - Bob Ross') # and displays it.

    @commands.command(aliases=['penis', 'penissize', 'dick'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dicksize(self, ctx):
        if ctx.author.id == 263883999687081984:
            await ctx.send('Your dick is so small it inverted on it\'s self and became a vagina.')
            return
        await ctx.send('8{}D'.format(random.randint(1, 25) * '='))

    @commands.command(aliases=['love', 'lovecalculator'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lovecalc(self, ctx, name, name2=None):
        await ctx.message.channel.trigger_typing()# triggers typing
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
        if name2 is not None:
            try:
                user2 = ctx.message.mentions[0]
            except IndexError:
                user2 = ctx.guild.get_member_named(name2)
            if not user2:
                user2 = ctx.guild.get_member(int(name2))
            if not user2:
                user2 = self.bot.get_user(int(name2))
        else:
            user2 = ctx.author
        async with aiohttp.ClientSession() as session: # opens session
            headers = {
                'X-Mashape-Key': 'GzMUj5WCc9mshdkqSfONZ2QmPTLsp1prbicjsntLl2T6SiuAeJ',
                'Accept': 'application/json'
            }
            params = {
                'fname': user.display_name,
                "sname": user2.display_name
            }
            async with session.get(f'https://love-calculator.p.mashape.com/getPercentage', params=params, headers=headers) as resp: # gets response
                data = await resp.json()
                await ctx.send(f'{user.display_name} :heart: {params["sname"]}\n{data["percentage"]}%, {data["result"]}')

    @commands.group(invoke_without_command=True, aliases=["math"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mathquiz(self, ctx):
        lower = -99
        upper = 99
        config = load_user_config(ctx)
        try:
            percent = round(100 * (config['users'][str(ctx.author.id)]['score']['right'] / (config['users'][str(ctx.author.id)]['score']['right'] + config['users'][str(ctx.author.id)]['score']['wrong'])), 2)
        except ZeroDivisionError:
            percent = 0
        if percent >= 70 and config['users'][str(ctx.author.id)]['score']['right'] >= 25:
            lower = -500
            upper = 500
        if percent >= 75 and config['users'][str(ctx.author.id)]['score']['right'] >= 50:
            lower = -1000
            upper = 1000
        if percent >= 80 and config['users'][str(ctx.author.id)]['score']['right'] >= 75:
            lower = -1500
            upper = 1500
        num1 = random.randint(lower, upper)
        num2 = random.randint(lower, upper)
        while num1 == num2:
            num2 = random.randint(lower, upper)
        operator = random.randint(1, 2)
        if operator == 1:
            num3 = num1 + num2
            operator = "+"
        elif operator == 2:
            num3 = num1 - num2
            operator = "-"
        else:
            print(operator)
        #print(num3)
        def mathcheck(m):
            #print(num3)
            #print(m.content)
            return m.author == ctx.author and m.channel == ctx.channel and m.content == str(num3)
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Quiz", description=f"Solve **{num1} {operator} {num2}**. You have **ten (10)** seconds.", color=0xffff00)
        await ctx.send(embed=embed)
        await ctx.message.channel.trigger_typing()
        config = load_user_config(ctx)
        try:
            await self.bot.wait_for('message', check=mathcheck, timeout=10)
            #print("right")
            #print(config['users'][str(ctx.author.id)]['score']['right'])
            config['users'][str(ctx.author.id)]['score']['right'] += 1
            #print(config['users'][str(ctx.author.id)]['score']['right'])
            try:
                percent = round(100 * (config['users'][str(ctx.author.id)]['score']['right'] / (config['users'][str(ctx.author.id)]['score']['right'] + config['users'][str(ctx.author.id)]['score']['wrong'])), 2)
            except ZeroDivisionError:
                percent = "NaN"
            embed = discord.Embed(title="Nice!", description=f"Total right (lifetime): {config['users'][str(ctx.author.id)]['score']['right']}\nTotal wrong (lifetime): {config['users'][str(ctx.author.id)]['score']['wrong']}\nPercent: {percent}%", color=0x00ff00)
            await ctx.send(embed=embed)
            write_to_user_config(ctx, config)
            return
        except asyncio.TimeoutError:
            #print('wrong')
            #print(config['users'][str(ctx.author.id)]['score']['wrong'])
            config['users'][str(ctx.author.id)]['score']['wrong'] += 1
            #print(config['users'][str(ctx.author.id)]['score']['wrong'])
            try:
                percent = round(100 * (config['users'][str(ctx.author.id)]['score']['right'] / (config['users'][str(ctx.author.id)]['score']['right'] + config['users'][str(ctx.author.id)]['score']['wrong'])), 2)
            except ZeroDivisionError:
                percent = "NaN"
            embed = discord.Embed(title="You took too long.", description=f"The answer was **{num3}**\nTotal right (lifetime): {config['users'][str(ctx.author.id)]['score']['right']}\nTotal wrong (lifetime): {config['users'][str(ctx.author.id)]['score']['wrong']}\nPercent: {percent}%", color=0xff0000)
            await ctx.send(embed=embed)
            write_to_user_config(ctx, config)
            return

    @mathquiz.command(aliases=["average", "mean"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def avg(self, ctx):
        await ctx.message.channel.trigger_typing()
        config = load_user_config(ctx)
        total_right = 0
        total_wrong = 0
        for user in config['users']:
            #print(user)
            total_right += config['users'][user]['score']['right']
            total_wrong += config['users'][user]['score']['wrong']
        avg = round(100 * (total_right / (total_wrong + total_right)), 2)
        total_attempts = total_right + total_wrong
        await ctx.send(f"Average: {avg}%\nTotal right: {total_right}\nTotal wrong: {total_wrong}\nTotal Attempts: {total_attempts}")

    @commands.command(aliases=['taco'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tacorecipe(self, ctx):
        try:
            await ctx.message.channel.trigger_typing() # trigger typing
            async with aiohttp.ClientSession() as session: # opens session
                async with session.get(f'http://taco-randomizer.herokuapp.com/random/') as resp: # gets response
                    resp = json.loads(await resp.read())
            taco_embeds = {}
            taco_embeds["0"] = discord.Embed(title="Shell", description=resp['shell']['recipe'], color=0xDAD790)
            taco_embeds["1"] = discord.Embed(title="Seasoning", description=resp['seasoning']['recipe'], color=0xff0000)
            taco_embeds["2"] = discord.Embed(title="Mixin", description=resp['mixin']['recipe'], color=0x00FF7F)
            taco_embeds["3"] = discord.Embed(title="Base Layer", description=resp['base_layer']['recipe'], color=0xe5b73b)
            taco_embeds["4"] = discord.Embed(title="Condiment", description=resp['condiment']['recipe'], color=0xFFFFFF)
            for ingredient in taco_embeds:
                await ctx.send(embed=taco_embeds[ingredient])
        except Exception as e:
            error = f"{type(e).__name__} : {e}"
            await ctx.send(error)

def setup(bot):
    bot.add_cog(fun(bot))