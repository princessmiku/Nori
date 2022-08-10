from ..sql import connection


def isAdmin(user_id: int) -> bool:
    answer = connection.table("users").select("administrator").where("id", user_id).fetchone()
    if answer is None: return False
    return bool(answer[0])


def isModerator(user_id: int) -> bool:
    answer = connection.table("users").select("moderator").where("id", user_id).fetchone()
    if answer is None: return False
    return bool(answer[0])


def isCreator(user_id: int) -> bool:
    answer = connection.table("users").select("creator").where("id", user_id).fetchone()
    if answer is None: return False
    return bool(answer[0])
