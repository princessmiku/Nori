from discord import Embed, Color

from . import defaultDesign


def cancelDesign() -> Embed:
    return defaultDesign(
        title="Cancel successful",
        description="The action was successfully canceled",
        color=Color.green()
    )
