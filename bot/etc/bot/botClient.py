from configparser import ConfigParser
from typing import Any

import discord
from discord import Intents, Message, Client
from discord.app_commands import CommandTree

from ..startup.checkExists import CheckExists
from ..startup.generateStructure import GenerateStructure


class BotClient(Client):
    checkExists = CheckExists()
    generateStructure = GenerateStructure(checkExists)
    config = ConfigParser(); config.read("./config/bot.ini")
    owner = config.getint("DISCORD", "bot_owner")

    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.tree = CommandTree(self)
        self.bot_guild = discord.Object(id=self.config.getint("DISCORD", "bot_guild"))


    async def on_ready(self):
        print(self.bot_guild)
        print("I'm online")

    async def on_message(self, message: Message) -> None:
        return

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=self.bot_guild)
        #await self.tree.sync(guild=self.bot_guild)


client = BotClient(intents=Intents.default())
