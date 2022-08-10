from discord import Interaction, InteractionResponse
from discord.app_commands import describe, choices, Choice
from etc.bot.botClient import client
from etc.modal.suggestionModal import Suggestion
from etc.language import lang


@client.tree.command(description="schlage einen eintrag vor")
@choices(language=[Choice(name=x, value=int(lang[x])) for x in lang])
async def suggestion(interaction: Interaction, language: Choice[int]):
    response: InteractionResponse = interaction.response
    print(language)
    sugModel = Suggestion(str(language.value))
    await response.send_modal(sugModel)
