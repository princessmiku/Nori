import time
from typing import Any

import discord
from discord import Interaction, Embed, Color, InteractionResponse
from discord.ui import View, Button, Select
from discord.ui.select import SelectOption
from scientist.datahandler.dtos_S2Data import Collection
from scientist.search import Record
from scientist.search.displayRecord import DRec

from ..google.result import Result
from ..sql import connection
from validators import url as isUrl
from ..search import sc
from ..google import embed_footer_text as g_embed_footer_text, logo_url as g_logo_url
from ..suggestion.create import add
from ..language import lang

_lastfeedback = {}
_tooMuchFeedback = {}


class _Select(Select):

    def __init__(self, drec: DRec, main_window, gResult: Result = None):
        options: list[SelectOption] = []
        if gResult:
            options.append(
                SelectOption(label=gResult.title[:85] + "..." if len(gResult.title) > 85 else gResult.title, emoji="🌐", value="google_search", description=gResult.description[:50])
            )
        self.r_options = {}
        x: Collection
        count = 0
        if drec is not None:
            for x in drec.get():
                options.append(
                    SelectOption(label=x.name[:85] + "..." if len(x.name) > 85 else x.name, emoji="🔎", value=x.identifier, description=', '.join(x.category)[:50]))
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
        self.gResult: Result = main_window.gResult
        self.searchText = main_window.searchText

    async def callback(self, interaction: Interaction) -> Any:
        if interaction.user.bot: return
        if _tooMuchFeedback.__contains__(interaction.user.id) and _tooMuchFeedback[interaction.user.id] > 5:
            await interaction.response.send_message(
                "you are unfortunately locked due to too much feedback in too short time",
                ephemeral=True
            )
            return
        if not _lastfeedback.__contains__(interaction.user.id) or _lastfeedback[interaction.user.id] + 30 > time.time():
            try:
                if _lastfeedback[interaction.user.id] + 30 > time.time():
                    if not _tooMuchFeedback.__contains__(interaction.user.id):
                        _tooMuchFeedback[interaction.user.id] = 0
                    else:
                        _tooMuchFeedback[interaction.user.id] += 1
                elif _lastfeedback[interaction] + _lastfeedback[interaction.user.id] + 300 > time.time():
                    _tooMuchFeedback.pop(interaction.user.id)
            except KeyError:
                pass
            _lastfeedback[interaction.user.id] = time.time()
            if self.dropdown.selected == "google_search":
                add(interaction.user.id,
                    self.gResult.title,
                    self.gResult.description,
                    self.gResult.url,
                    self.searchText,
                    lang["german"], True,
                    self.gResult.image
                    )
                await interaction.response.send_message(
                    "thank you for your feedback. The result will be added to the database",
                    ephemeral=True
                )
                sc.recreateIndex()
            else:
                self.record.setResult(self.dropdown.r_options[self.dropdown.selected])
                sc.insertRecord(self.record)
                await interaction.response.send_message(
                    "thank you for your feedback",
                    ephemeral=True
                )
        else:
            await interaction.response.send_message(
                "this button has a cooldown, please wait a moment and try again",
                ephemeral=True
            )


class SearchDrop(View):

    def __init__(self, record: Record, gResult: Result, searchText: str):
        self.record = record
        self.searchText = searchText
        if record is None:
            self.drec = None
        else:
            self.drec = record.getAsDRec(19)
        self.gResult = gResult
        self.dropdown = _Select(self.drec, self, gResult)
        if gResult:
            self.sourceB = _SourceButton(
                gResult.url
            )
        elif record != None:
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
        try:
            self.add_item(self.sourceB)
        except:
            pass

    async def render(self, interaction: Interaction):
        self.remove_item(self.sourceB)
        if self.dropdown.selected == "google_search":
            embed = renderEmbed(self.dropdown.selected, self.gResult, True)
            self.sourceB = _SourceButton(self.gResult.url)
        else:
            theUrl = connection.table("qaa")\
                .select("sources")\
                .where("id", int(self.dropdown.selected))\
                .fetchone()[0]
            embed = renderEmbed(self.dropdown.selected)
            self.sourceB = _SourceButton(theUrl)
        self.add_item(self.sourceB)
        await interaction.response.edit_message(embed=embed, view=self)


def renderEmbed(identifier: str, data=None, isGoogle: bool = False) -> Embed:
    if isGoogle:
        data: Result
        embed = Embed(
            title=data.title,
            description=data.description,
            color=0x0F71F2
        ).set_footer(
            text=g_embed_footer_text,
            icon_url=g_logo_url
        )
        if data.image:
            embed.set_image(url=data.image)
        return embed
    else:
        data: list = connection.table("qaa").select("question, answer, image").where("id", int(identifier)).fetchone()
        embed = Embed(
            title=data[0],
            description=data[1],
            color=Color.yellow()
        )
        #if data[2]:
        embed.set_image(url=data[2])
        return embed
