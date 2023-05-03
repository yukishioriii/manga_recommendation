from typing import List
from pymongo import MongoClient


class MangaDatabase():
    client = MongoClient()
    db = client["manga_recc"]
    manga_collection = db["manga"]

    def _create_update_query(self, manga_individual):
        query = {"_id": manga_individual["_id"]}
        update = {"$set": manga_individual}
        upsert = True
        return query, update, upsert

    def insert_manga(self, manga: List):
        try:
            for i in manga:
                self.manga_collection.update_one(*self._create_update_query(i))
        except Exception as e:
            raise Exception(f"EXEPTION:[DB] @ {i} \n {e}")
