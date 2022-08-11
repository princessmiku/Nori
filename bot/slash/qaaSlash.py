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
        if len(record.data) == 0:
            await response.send_message("nothing found")
            return
        view = SearchDrop(record)
        _id = view.dropdown.options[0].value
        await response.send_message(embed=renderEmbed(_id), view=SearchDrop(record))
