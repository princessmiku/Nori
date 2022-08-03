import threading

from discord import Member
from datetime import datetime

from ..sql import connection


def insert(member: Member):
    if not connection.table("users").exists().where("id", member.id).checkExists():
        connection.table("users").insert()\
            .set("id", member.id)\
            .set("createAt", datetime.today().strftime('%H:%M:%S on %B %d, %Y'))\
            .set("username", member.name)\
            .ignore()\
            .execute()
