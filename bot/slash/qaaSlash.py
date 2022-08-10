from discord import Interaction, InteractionResponse
from scientist.search import Record
from scientist.search.displayRecord import DRec

from etc.bot.botClient import client
from etc.modal.searchModal import SearchModal
from etc.search import sc
from etc.search.searchDropdown import SearchDrop, renderEmbed


@client.tree.command(description="search in the Q&A")
async def search(interaction: Interaction, text: str = None):
    response: InteractionResponse = interaction.response
    if text is None:
        await response.send_modal(SearchModal())
    else:
        record: Record = sc.match(text)
        drec: DRec = DRec(record, 24)
        if len(drec.get()) == 0:
            await response.send_message("nothing found")
            return
        view = SearchDrop(drec)
        _id = view.dropdown.options[0].value
        await response.send_message(embed=renderEmbed(_id), view=SearchDrop(drec))
