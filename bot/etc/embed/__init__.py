from discord import Color, Embed


def defaultDesign(title: str = None, description: str = None, color: Color = Color.orange()) -> Embed:
    embed: Embed = Embed(description=description, title=title, color=color)
    return embed
