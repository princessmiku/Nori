from discord import TextStyle, Interaction, InteractionResponse
from discord.ui import Modal, TextInput, Select
from discord.ui.select import SelectOption
from ..sql import connection
from ..language import lang


class Suggestion(Modal, title="Suggestion"):
    about = TextInput(
        label="About",
        style=TextStyle.long,
        default="Information about this modal.\n"
                "Here you can suggest an entry in the Q&A\n"
                "Only entries that conform to the rules are allowed, use the slash provided for this (in progress).",
                #"\n\nLanguage | The Default language is english or the selected language in the slash option"
        required=False
    )
    question = TextInput(
        label="Question",
        placeholder="Question of the faq",
        min_length=5,
        max_length=300,
        required=True,
        row=2
    )
    answer = TextInput(
        label="What is the answer to the question?",
        style=TextStyle.long,
        placeholder='Write here your text or the url',
        min_length=10,
        max_length=1500,
        required=True,
        row=3
    )
    source = TextInput(
        label="Source",
        style=TextStyle.long,
        placeholder="list your sources here, if available",
        required=False,
        min_length=15,
        max_length=1500,
        row=4
    )

    def __init__(self, language: str = "1"):
        super().__init__()
        #options = [SelectOption(label=x, value=str(lang[x])) for x in lang.keys()]
        self.timeout = 360
        #self.sel = Select(
        #    options=options,
        #    row=1,
        #    placeholder="Language",
        #    max_values=1,
        #    min_values=0
        #)
        self.language = language
#
        #self.add_item(self.sel)

    async def on_submit(self, interaction: Interaction) -> None:
        connection.table("qaa").insert()\
            .set("author_id", interaction.user.id)\
            .set("question", self.question.value)\
            .set("answer", self.answer.value)\
            .set("source", self.source.value)\
            .set("language", self.language)\
            .execute()
        response: InteractionResponse = interaction.response
        await response.send_message("Thank you for your suggestion, it will now be checked and included", ephemeral=True)

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        pass
