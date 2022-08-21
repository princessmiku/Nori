from ..search import sc
from ..sql import connection
from ..language import langR


def add(user_id: int, question: str, answer: str, source: str, tags: str, language: str, google: bool = False, image: str = None):
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
