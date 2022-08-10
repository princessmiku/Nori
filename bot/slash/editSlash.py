from typing import Literal

import discord
from discord import Interaction, InteractionResponse, User
from discord.app_commands import describe, choices, Choice, Group, command
from etc.bot.botClient import client
from etc.modal.suggestionModal import Suggestion
from etc.language import lang
from etc.permission import isAdmin, isCreator, isModerator
from etc.embed.permission import invalidPermissions
from etc.embed.inputEmbed import botMentionNotAllowed
from etc.sql import connection
from etc.search import sc


class Editor(Group):

    editor = Group(name="editor", description="edit tool for stuff and creator")

    @command(name="qaa", description="edit the q&a")
    async def edit_qaa(self, interaction: Interaction, id: int, option: Literal["edit", "delete"]):
        if not isCreator(interaction.user.id):
            await interaction.response.send_message(embed=invalidPermissions(), ephemeral=True)
            return
        await interaction.response.send_message("slash in development", ephemeral=True)

    @command(name="permission", description="edit user permission | only for admin")
    async def edit_perm(self,
                        interaction: Interaction,
                        user: User,
                        perm: Literal["creator", "moderator", "administrator", "delete"]):
        """"""
        response: InteractionResponse = interaction.response
        if not isAdmin(interaction.user.id):
            await response.send_message(embed=invalidPermissions(), ephemeral=True)
            return
        if user.bot:
            await response.send_message(embed=botMentionNotAllowed(), ephemeral=True)
            return
        if user.id == client.owner:
            await response.send_message(embed=invalidPermissions(), ephemeral=True)
            return
        client.wait_for('message')
        if perm == "delete":
            connection.table("users").delete().where("id", user.id).execute()
            await response.send_message(embed=discord.Embed(
                description=f"Successful remove all permissions from {user.mention}"
            ), ephemeral=True)
        elif perm == "creator":
            connection.table("users").upsert()\
                .set("creator", 1)\
                .set("moderator", 0)\
                .set("administrator", 0)\
                .set("id", user.id)\
                .execute()
            await response.send_message(embed=discord.Embed(
                description=f"Successful set permission level `creator` on {user.mention}"
            ), ephemeral=True)
        elif perm == "moderator":
            connection.table("users").upsert() \
                .set("creator", 1) \
                .set("moderator", 1) \
                .set("administrator", 0) \
                .set("id", user.id) \
                .execute()
            await response.send_message(embed=discord.Embed(
                description=f"Successful set permission level `moderator` on {user.mention}"
                            f"\nThe `moderator` permissions include the permission for `creator`"
            ), ephemeral=True)
        elif perm == "administrator":
            connection.table("users").upsert() \
                .set("creator", 1) \
                .set("moderator", 1) \
                .set("administrator", 1) \
                .set("id", user.id) \
                .execute()
            await response.send_message(embed=discord.Embed(
                description=f"Successful set permission level `administrator` on {user.mention}"
                            f"\nThe `administrator` permissions include the permission for `creator` and `moderator`"
            ), ephemeral=True)

    @command(name="user", description="edit all user")
    async def edit_user(self, interaction: Interaction, user: User, option: Literal["block", "unblock"]):
        if not isModerator(interaction.user.id):
            await interaction.response.send_message(embed=invalidPermissions(), ephemeral=True)
            return
        await interaction.response.send_message("slash in development", ephemeral=True)

    @command(name="recreate", description="recreate the internal search index")
    async def recreate(self, interaction: Interaction):
        if not isModerator(interaction.user.id):
            await interaction.response.send_message(embed=invalidPermissions(), ephemeral=True)
            return
        await interaction.response.send_message("index will recreate", ephemeral=True)
        sc.recreateIndex()


client.tree.add_command(Editor())
