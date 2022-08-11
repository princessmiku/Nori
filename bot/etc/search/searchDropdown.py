import time
from typing import Any

import discord
from discord import Interaction, Embed, Color, InteractionResponse
from discord.ui import View, Button, Select
from discord.ui.select import SelectOption
from scientist.datahandler.dtos_S2Data import Collection
from scientist.search import Record
from scientist.search.displayRecord import DRec
from ..sql import connection
from validators import url as isUrl
from ..search import sc

_lastfeedback = {}


class _Select(Select):

    def __init__(self, drec: DRec, main_window):
        options = []
        self.r_options = {

        }
        x: Collection
        count = 0
        for x in drec.get():
            options.append(
                SelectOption(label=x.name, emoji="🔎", value=x.identifier, description=', '.join(x.category)[:50]))
            self.r_options[x.identifier] = count
            count += 1
        self.selected = options[0].value
        super().__init__(options=options)
        self.main_window = main_window
        self.row = 0

    async def callback(self, interaction: Interaction) -> Any:
        self.selected = self.values[0]
        await self.main_window.render(interaction)


class _SourceButton(Button):

    def __init__(self, url: str):
        if isUrl(url):
            self.sendUrls = False
            super().__init__(label="Source", emoji="📎", url=url)
        else:
            super().__init__(label="Source", emoji="📎")
            self.sendUrls = True
            self.urlList = url

    async def callback(self, interaction: Interaction) -> Any:
        if self.sendUrls:
            await interaction.response.send_message(
                embed=Embed(
                    description=self.urlList.replace(" ", "\n"),
                    color=Color.teal(),
                    title="Sources"
                ),
                ephemeral=True
            )


class _RightB(Button):
    def __init__(self, main_window):
        super().__init__(label="Found it", emoji="👍")
        self.record: Record = main_window.record
        self.dropdown = main_window.dropdown

    async def callback(self, interaction: Interaction) -> Any:
        if interaction.user.bot: return
        if not _lastfeedback.__contains__(interaction.user.id) or _lastfeedback[interaction.user.id] + 30 > time.time():
            _lastfeedback[interaction.user.id] = time.time()
            self.record.setResult(self.dropdown.r_options[self.dropdown.selected])
            sc.insertRecord(self.record)
        await interaction.response.send_message(
            "thank you for your feedback",
            ephemeral=True
        )


class SearchDrop(View):

    def __init__(self, record: Record):
        self.record = record
        self.drec = record.getAsDRec(24)
        self.dropdown = _Select(self.drec, self)
        self.sourceB = _SourceButton(
            connection.table("qaa")
                .select("sources")
                .where("id", int(self.dropdown.selected))
                .fetchone()[0]
        )
        self.rightB = _RightB(self)
        super().__init__()
        self.add_item(self.dropdown)
        self.add_item(self.rightB)
        self.add_item(self.sourceB)

    async def render(self, interaction: Interaction):
        data = connection.table("qaa")\
            .select("question, answer, sources, tags")\
            .where("id", int(self.dropdown.selected))\
            .fetchone()
        embed = renderEmbed(self.dropdown.selected, data)
        self.remove_item(self.sourceB)
        self.sourceB = _SourceButton(data[2])
        self.add_item(self.sourceB)
        await interaction.response.edit_message(embed=embed, view=self)


def renderEmbed(identifier: str, data=None) -> Embed:
    if data is None: data = connection.table("qaa").select("question, answer").where("id", int(identifier)).fetchone()
    return Embed(
        title=data[0],
        description=data[1],
        color=Color.teal()
    )
