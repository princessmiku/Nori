import json

from ..search import sc
from ..sql import connection
from ..language import langR


def add(user_id: int, question: str, answer: str, source: str, tags: str, language: str, google: bool = False, image: str = None):
    if google:
        result = connection.table("qaa").select("id, question, tags").where("question", question).fetchone()
        print(result)
        if result:
            theTags: list = result[2].split(", ")
            if not theTags.__contains__(tags):
                theTags.append(tags)
                connection.table("qaa").update().where("id", result[0]).set("tags", ", ".join(theTags)).execute()
            return
    connection.table("qaa").insert() \
        .set("author_id", user_id) \
        .set("question", question) \
        .set("answer", answer) \
        .set("sources", source) \
        .set("lang", language) \
        .set("tags", tags) \
        .set("google_search", int(google)) \
        .set("image", image) \
        .execute()
    _id = connection.table("qaa").select("id").where("question", question).where("lang", language).fetchone()[0]

    sc.addElement(
        name=question,
        identifier=str(_id),
        _category=tags.replace(", ", ",").split(",").append(langR[language]),
        extraSearchs=answer
    )
