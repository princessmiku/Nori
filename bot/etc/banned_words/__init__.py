import os
from glob import glob
from urllib.parse import unquote
from threading import Thread
print(glob("./config/banned_words/*.txt"))
chunk_size: int = 10
_raw_word_list: list[str] = [
    j for i in
    [unquote(open("./config/banned_words/"+y, mode='r', encoding='utf-8').read()).split("\n") for y in os.listdir("./config/banned_words") if y.endswith(".txt")]
    for j in i
]
list_of_words: list[list[str]] = [
    _raw_word_list[i:i + chunk_size]
    for i in range(0, len(_raw_word_list), chunk_size)
]


def check_BadWord(text: str) -> bool:
    result: list[bool] = []

    def _check(text: str, bList: list[str]):
        print("start")
        if any(word in text for word in bList): result.append(True)
    #threads = [x for x in list_of_words]
    print(list_of_words)
    threads: list[Thread] = [Thread(target=_check, args=(text, bList,), daemon=True) for bList in list_of_words]
    [x.start() for x in threads]
    [x.join() for x in threads]
    print(threads)
    return result.__contains__(True)
