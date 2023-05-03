from typing import Tuple
import requests
from database import MangaDatabase
MANGA_LIST_API = "https://api.mangadex.org/manga"


class MangaDexAPI():

    def _query_builder(self, query):
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

    def _create_param(self, limit, offset=0):

        param = {
            "availableTranslatedLanguage": ["en"],
            # "includedTags": [""],
            "publicationDemographic": ["josei", "seinen"],
            "order": {"rating": "desc"},
            "hasAvailableChapters": "true",
            "limit": limit,
            "offset": offset
        }
        return self._query_builder(param), offset+limit

    def get_anime(self):
        headers = {}
        max_count = 30
        next_offset = 0
        data = []
        while next_offset < max_count:
            param, next_offset = self._create_param(
                limit=10, offset=next_offset)
            resp = requests.get(MANGA_LIST_API + param, headers=headers)
            if resp.status_code == 200:
                data.extend(resp.json()["data"])
            else:
                raise Exception(
                    f"EXEPTION:[API] stopped at {next_offset} with\n {resp.json()}, ")
        return data


if __name__ == "__main__":
    a = MangaDexAPI()
    db = MangaDatabase()
    data = a.get_anime()
    db.insert_manga([{**i, "_id": i["id"]} for i in data])
