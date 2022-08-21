from ..google.result import Result
from wikipedia import page as s_page
import wikipedia
wikipedia.set_lang("de")


def search(url: str):
    q = url.rsplit("/", 1)[-1]
    page = s_page(q)
    return Result(
        title=q,
        description=page.content,
        url=page.url,
        image=page.images[0]
    )
