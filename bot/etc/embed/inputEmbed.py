from discord import Embed, Color


def botMentionNotAllowed() -> Embed:
    return Embed(
        description="The mention of bots is not allowed here",
        color=Color.red()
    )
