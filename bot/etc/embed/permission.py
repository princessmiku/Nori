from discord import Embed, Color


def invalidPermissions() -> Embed:
    return Embed(
        color=Color.red(),
        description="Invalid permissions for this slash"
    )
