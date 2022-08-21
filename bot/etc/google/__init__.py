
# google api
g_apiKey = open("./config/google_api_key.txt", mode='r').read()

# embed decoration
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.png"
embed_footer_text = "searched with google"


# url blacklist

url_blacklist: list[str] = []
with open('./config/url_blacklist.txt', mode='r') as _bFile:
    url_blacklist += _bFile.read().split("\n")
    _bFile.close()


def addURL_ToBlacklist(url: str):
    url_blacklist.append(url)
    with open('./config/url_blacklist.txt', mode='a') as file:
        file.write(url + "\n")
        file.close()

