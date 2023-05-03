import requests
MANGA_LIST_API = "https://api.mangadex.org/manga"


def query_builder(query):
    res = "?"
    for key, value in query.items():
        if type(value) is list:
            res += "&".join([f"{key}[]={i}" for i in value])
        elif type(value) is dict:
            res += key
            for k, v in value.items():
                res += f"[{k}]={v}"
        else:
            res += f"{key}={value}"
        res += "&"
    return res[:-1]


def get_anime():
    headers = {}
    offset = 0
    params = {
        "availableTranslatedLanguage": ["en"],
        # "includedTags": [""],
        "publicationDemographic": ["josei", "seinen"],
        "order": {"rating": "desc"},
        "hasAvailableChapters": "true",
        "limit": 10,
        "offset": offset
    }
    url = query_builder(params)
    resp = requests.get(MANGA_LIST_API + url, headers=headers)
    print(resp.json())


if __name__ == "__main__":
    get_anime()
