from discord import TextStyle, Interaction, InteractionResponse
from discord.ui import Modal, TextInput, Select
from discord.ui.select import SelectOption
from ..sql import connection
from ..language import lang
from ..suggestion import create


class Suggestion(Modal, title="Suggestion"):
    #about = TextInput(
    #    label="About",
    #    style=TextStyle.long,
    #    default="Information about this modal.\n"
    #            "Here you can suggest an entry in the Q&A\n"
    #            "Only entries that conform to the rules are allowed, use the slash provided for this (in progress).",
    #    required=False
    #)
    question = TextInput(
        label="Question | Title",
        placeholder="Question of the Q&A",
        min_length=5,
        max_length=300,
        required=True
    )
    answer = TextInput(
        label="What is the answer to the question?",
        style=TextStyle.long,
        placeholder='Write here your text or the url',
        min_length=10,
        max_length=1500,
        required=True
    )
    source = TextInput(
        label="Source",
        style=TextStyle.long,
        placeholder="list your sources here, if available",
        required=False,
        min_length=15,
        max_length=1500
    )
    tags = TextInput(
        label="Tags",
        style=TextStyle.long,
        placeholder="search tags, separate with ','",
        required=False,
        max_length=100
    )

    def __init__(self, language: str = "1"):
        self.language = language
        super().__init__()
        self.timeout = 360

    async def on_submit(self, interaction: Interaction) -> None:
        create.add(
            interaction.user.id,
            self.question.value,
            self.answer.value,
            self.source.value,
            self.tags.value,
            self.language
        )
        response: InteractionResponse = interaction.response
        await response.send_message(
            "Thank you for your suggestion, it will now be checked and included",
            ephemeral=True
        )

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        print(error)
