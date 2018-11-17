import asyncio
import datetime
import json
import logging
from pathlib import Path

import discord
from discord.ext import commands

# https://discordapp.com/oauth2/authorize?client_id=500165490753404938&scope=bot&permissions=8

# APPROVED SERVERS:
# Fooeyy Official - 476519720380792834


def config_load():
    with open("data/config.json", "r", encoding="utf-8") as doc:
        #  Please make sure encoding is correct, especially after editing the config file
        return json.load(doc)


def guild_config_load(gid):
    with open(f"data/servers/{gid}/config.json", "r", encoding="utf-8") as doc:
        return json.load(doc)


async def run():
    """
    Where the bot gets started. If you wanted to create an database connection pool or other session for the bot to use,
    it's recommended that you create it here and pass it to the bot as a kwarg.
    """

    config = config_load()
    bot = Bot(config=config, description=config["description"] + config["prefix"])
    try:
        await bot.start(config["token"])
    except KeyboardInterrupt:
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix_, description=kwargs.pop("description")
        )
        self.start_time = None
        self.app_info = None

        self.loop.create_task(self.track_start())
        self.loop.create_task(self.load_all_extensions())

    async def track_start(self):
        """
        Waits for the bot to connect to discord and then records the time.
        Can be used to work out uptime.
        """
        await self.wait_until_ready()
        self.start_time = datetime.datetime.utcnow()

    async def get_prefix_(self, bot, message):
        """
        A coroutine that returns a prefix.

        I have made this a coroutine just to show that it can be done. If you needed async logic in here it can be done.
        A good example of async logic would be retrieving a prefix from a database.
        """
        config = config_load()
        prefix = [config["prefix"]]
        return commands.when_mentioned_or(*prefix)(bot, message)

    async def load_all_extensions(self):
        """
        Attempts to load all .py files in /cogs/ as cog extensions
        """
        await self.wait_until_ready()
        await asyncio.sleep(
            1
        )  # ensure that on_ready has completed and finished printing
        cogs = [x.stem for x in Path("cogs").glob("*.py")]
        for extension in cogs:
            try:
                self.load_extension(f"cogs.{extension}")
                print(f"loaded {extension}")
            except Exception as e:
                error = f"{extension}\n {type(e).__name__} : {e}"
                print(f"failed to load extension {error}")
            print("-" * 10)

    async def on_ready(self):
        """
        This event is called every time the bot connects or resumes connection.
        """
        self.remove_command("help")
        # await self.change_presence(activity=discord.Game(name='Version 2.0'))
        print("-" * 10)
        self.app_info = await self.application_info()
        print(
            f"Logged in as: {self.user.name}\n"
            f"Using discord.py version: {discord.__version__}\n"
            f"Owner: {self.app_info.owner}"
        )
        print("-" * 10)

    async def on_message(self, message):
        """
        This event triggers on every message received by the bot. Including one's that it sent itself.

        If you wish to have multiple event listeners they can be added in other cogs. All on_message listeners should
        always ignore bots.
        """
        config = config_load()
        if isinstance(message.channel, discord.TextChannel):
            guild_config = guild_config_load(message.guild.id)
            # print(guild_config)
            # print(guild_config['lockdownmode'])
            if (
                guild_config["lockdownmode"]
                and not message.author.guild_permissions.administrator
            ):
                await message.delete()
        if message.author.id == 263_883_999_687_081_984 and config["fuck_with_gennate"]:
            await message.delete()
            return
        if message.author.bot and message.content != "Pong!":
            return  # ignore all bots
        if not isinstance(
            message.channel, discord.TextChannel
        ) and message.content.startswith(config["prefix"]):
            return  # ignore all private message commands
        if not isinstance(message.channel, discord.TextChannel):
            await self.process_commands(message)
            return
        with open(
            f"data/servers/{message.guild.id}/blacklist.txt", "r"
        ) as blacklistfile:
            blacklist = blacklistfile.read().splitlines()

        for line in blacklist:
            if (
                line.lower() in message.content.lower()
                and message.author.id != 146_151_306_216_734_720
                and not message.author.guild_permissions.administrator
            ):
                await message.delete()
                await message.channel.send(
                    f"You said a blacklisted word/phrase/url, <@{message.author.id}>. Don't say it again."
                )
                return

        if message.channel.id == 464_681_103_970_795_521 and not (
            "youtube.com" in message.content or "youtu.be" in message.content
        ):
            await message.delete()
            await message.author.send(
                "Only youtube links are allowed in the youtube selfpromo channel."
            )
            return

        if (
            message.channel.id == 464_681_092_319_019_008
            and not "twitch.tv" in message.content
        ):
            await message.delete()
            await message.author.send(
                "Only twitch links are allowed in the twitch selfpromo channel."
            )
            return

        if message.guild.id == 476_519_720_380_792_834 and not (
            message.channel != 477_682_348_880_560_128
            and message.channel != 477_198_878_429_413_416
        ):
            return

        if message.author.id == 146_151_306_216_734_720:
            if message.content.startswith("^reload "):
                extension = message.content[8:]
                try:
                    self.unload_extension(f"cogs.{extension}")
                    self.load_extension(f"cogs.{extension}")
                    await message.channel.send(f"Succesfully reloaded `{extension}`")
                    print(f"reloaded {extension}")
                    print("-" * 10)
                except Exception as e:
                    error = f"{extension}\n {type(e).__name__} : {e}"
                    await message.channel.send(f"Failed to reload cog {error}")
                return
            if message.content.startswith("^load "):
                extension = message.content[6:]
                try:
                    self.load_extension(f"cogs.{extension}")
                    await message.channel.send(f"Succesfully loaded `{extension}`")
                    print(f"loaded {extension}")
                    print("-" * 10)
                except Exception as e:
                    error = f"{extension}\n {type(e).__name__} : {e}"
                    await message.channel.send(f"Failed to load cog {error}")
                return
            if message.content.startswith("^unload "):
                extension = message.content[8:]
                try:
                    self.unload_extension(f"cogs.{extension}")
                    await message.channel.send(f"Succesfully unloaded `{extension}`")
                    print(f"unloaded {extension}")
                    print("-" * 10)
                except Exception as e:
                    error = f"{extension}\n {type(e).__name__} : {e}"
                    await message.channel.send(f"Failed to unload cog {error}")
                return
        await self.process_commands(message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
