from discord import Interaction, InteractionResponse
from discord.app_commands import describe, choices, Choice
from etc.bot.botClient import client
from etc.modal.suggestionModal import Suggestion
from etc.language import lang
from etc.permission import isCreator
from etc.embed.permission import invalidPermissions


@client.tree.command(description="suggest an Q&A entry")
@choices(language=[Choice(name=x, value=int(lang[x])) for x in lang])
async def suggestion(interaction: Interaction, language: Choice[int]):
    response: InteractionResponse = interaction.response
    if not isCreator(interaction.user.id):
        await response.send_message(embed=invalidPermissions(), ephemeral=True)
        return
    sugModel = Suggestion(lang[language.name])
    await response.send_modal(sugModel)
