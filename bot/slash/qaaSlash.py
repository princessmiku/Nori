import discord
from discord import Interaction, InteractionResponse
from scientist.search import Record
from scientist.search.displayRecord import DRec

from etc.bot.botClient import client
from etc.google.result import Result
from etc.modal.searchModal import SearchModal
from etc.search import sc
from etc.search.searchDropdown import SearchDrop, renderEmbed
from etc.google.search import search as g_search


@client.tree.command(description="search in the Q&A")
async def search(interaction: Interaction, text: str):
    response: InteractionResponse = interaction.response
    result: Result = None
    record = None
    try:
        record: Record = sc.match(text)
        if len(record.data) == 0 or record.highestRevel < 2.5:
            await response.defer(thinking=True)
            result: Result = g_search(text)
    except ValueError:
        await response.defer(thinking=True)
        result: Result = g_search(text)

    view = SearchDrop(record, result, text.lower())
    _id = view.dropdown.options[0].value
    if result:
        if response.is_done():
            await interaction.edit_original_response(embed=renderEmbed(_id, result, True), view=view)
        else:
            await response.send_message(embed=renderEmbed(_id, result, True), view=view)
    else:
        if record is not None:
            if response.is_done():
                await interaction.edit_original_response(embed=renderEmbed(_id), view=view)
            else:
                await response.send_message(embed=renderEmbed(_id), view=view)
        else:
            if response.is_done():
                await interaction.edit_original_response(content="The entire Internet has no answer to your question")
            else:
                await response.send_message("The entire Internet has no answer to your question")
