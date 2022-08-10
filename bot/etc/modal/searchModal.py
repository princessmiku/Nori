from discord import Interaction
from discord.ui import Modal, TextInput
from scientist.search import Record
from scientist.datahandler.dtos_S2Data import Collection
from scientist.search.displayRecord import DRec

from ..search import sc


class SearchModal(Modal, title="Search"):
    searchText = TextInput(
        label="What are you looking for?",
        max_length=100,
        min_length=3
    )

    async def on_submit(self, interaction: Interaction) -> None:
        record: Record = sc.match(self.searchText.value)
        drec: DRec = DRec(record, 20)
        await interaction.response.send_message()

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        print(error)
