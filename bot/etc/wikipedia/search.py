from ..google.result import Result
from wikipedia import page as s_page
from urllib.parse import unquote
import wikipedia
wikipedia.set_lang("de")


def search(url: str):
    url = unquote(url)
    q = url.rsplit("/", 1)[-1].split("#")[0].replace("_", " ")
    page = s_page(q)
    image = None
    if len(page.images) > 0:
        image = page.images[0]
    return Result(
        title=q,
        description=page.content.split("=")[0].replace("\n\n", ""),
        url=page.url,
        image=image
    )
