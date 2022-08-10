from typing import Any

from discord import Interaction, Embed, Color, InteractionResponse
from discord.ui import View, Button, Select
from discord.ui.select import SelectOption
from scientist.datahandler.dtos_S2Data import Collection
from scientist.search.displayRecord import DRec
from ..sql import connection


class _Select(Select):

    def __init__(self, drec: DRec, main_window):
        options = []
        x: Collection
        print(drec.get())
        for x in drec.get():
            options.append(SelectOption(label=x.name, emoji="🔎", value=x.identifier, description=', '.join(x.category)[:100]))
        self.selected = options[0].value
        super().__init__(options=options)
        self.main_window = main_window
        self.row = 0

    async def callback(self, interaction: Interaction) -> Any:
        self.selected = self.values[0]
        await self.main_window.render(interaction)


class _NextButton(Button):

    def __init__(self, drec: DRec, main_window):
        super().__init__(label="Next", emoji="➡")
        self.drec = drec
        self.main_window = main_window
        self.row = 1

    async def callback(self, interaction: Interaction) -> Any:
        success = self.drec.nextPage()
        if not success:
            await interaction.response.defer()
            return
        await self.main_window.render(interaction, True)


class _PreButton(Button):

    def __init__(self, drec: DRec, main_window):
        super().__init__(label="Previous", emoji="⬅")
        self.drec = drec
        self.main_window = main_window
        self.row = 1

    async def callback(self, interaction: Interaction) -> Any:
        success = self.drec.previousPage()
        if not success:
            await interaction.response.defer()
            return
        await self.main_window.render(interaction, True)


class SearchDrop(View):

    def __init__(self, drec: DRec):
        self.drec = drec
        self.dropdown = _Select(drec, self)
        self.nButton = _NextButton(drec, self)
        self.pButton = _PreButton(drec, self)
        super().__init__()
        self.add_item(self.dropdown)
        self.add_item(self.pButton)
        self.add_item(self.nButton)

    async def render(self, interaction: Interaction, newSite: bool = False):
        if newSite:
            self.remove_item(self.dropdown)
            self.dropdown = _Select(self.drec, self)
            self.add_item(self.dropdown)
            embed = renderEmbed(self.dropdown.options[0].value)
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            embed = renderEmbed(self.dropdown.selected)
            await interaction.response.edit_message(embed=embed)



def renderEmbed(identifier: str) -> Embed:
    data = connection.table("qaa").select("question, answer").where("id", int(identifier)).fetchone()
    return Embed(
        title=data[0],
        description=data[1],
        color=Color.teal()
    )
