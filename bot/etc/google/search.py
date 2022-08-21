from urllib.error import HTTPError
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from . import addURL_ToBlacklist, url_blacklist
from ..wikipedia.search import search as wiki_search
from .result import Result
from googlesearch import search as g_search


def get_hostname(url: str) -> str:
    parsed_uri = urlparse(url)
    return parsed_uri.hostname.split(".")[1].lower()


def route_function(url: str):
    hostname = get_hostname(url)
    print(url)
    if hostname == "wikipedia":
        return wiki_search(url)
    if hostname == "wikimedia":
        return wiki_search(url.rsplit("/", 1)[-1].replace("File:", "").split("_")[0])
    else:
        return google_scrape(url)


def google_scrape(url: str):
    thepage = urlopen(url)
    soup = BeautifulSoup(thepage, "html.parser")
    metas = soup.find_all('meta')
    meta_str = [meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description']
    return Result(
        title=soup.title.text,
        description='\n'.join(meta_str),
        url=url
    )


def search(q: str) -> Result:
    try:
        image = None
        for i in g_search(q, num=10, stop=2, pause=2, safe="on", country="de"):
            if str(urlparse(i).hostname) in url_blacklist: continue
            try:
                result: Result = route_function(i)
                if result.image or image is None: return result
                return result
            except HTTPError as e:
                if e.code == 403:
                    addURL_ToBlacklist(str(urlparse(i).hostname))
            except Exception as e:
                pass
    except:
        pass
    return Result(
        "Rick Astley - Never Gonna Give You Up (Official Music Video)",
        "*This is an error message*\n\n"
        "The official video for “Never Gonna Give You Up” by Rick Astley Taken from the album "
        "‘Whenever You Need Somebody’ – deluxe 2CD and digital deluxe out 6th May 2022 Pre-order "
        "here – https://RickAstley.lnk.to/WYNS2022ID",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
