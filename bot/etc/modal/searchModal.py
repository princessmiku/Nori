from discord import Interaction
from discord.ui import Modal, TextInput
from scientist.search import Record
from scientist.datahandler.dtos_S2Data import Collection
from scientist.search.displayRecord import DRec

from ..search import sc
from ..search.searchDropdown import SearchDrop, renderEmbed


class SearchModal(Modal, title="Search"):
    searchText = TextInput(
        label="What are you looking for?",
        max_length=100,
        min_length=3
    )

    async def on_submit(self, interaction: Interaction) -> None:
        record: Record = sc.match(self.searchText.value)
        drec: DRec = DRec(record, 24)
        if len(drec.get()) == 0:
            await interaction.response.send_message("nothing found")
            return
        view = SearchDrop(drec)
        _id = view.dropdown.options[0].value
        await interaction.response.send_message(embed=renderEmbed(_id), view=SearchDrop(drec))

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        print(error)
