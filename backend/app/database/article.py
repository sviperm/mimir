from typing import Any, Dict, List, Optional, Union

from bson.objectid import ObjectId

from database import (article_collection, course_collection,
                      curriculum_collection, user_collection)

__schema_version = "1.0"


async def insert_article(owner_id: str,
                         name: str,
                         slug: str,
                         is_draft: bool = False,
                         content: Optional[List[Dict]] = None,
                         *args,
                         **kwargs) -> Dict[str, Any]:
    document = {
        "_schema": __schema_version,
        "owner_id": owner_id,
        "name": name,
        "slug": slug,
        "is_draft": is_draft,
        "content": content,
    }
    article = await article_collection.insert_one(document)
    article = await get_article(article.inserted_id)
    return article


async def get_article(article_id: Union[str, ObjectId], *args, **kwargs) -> Dict:
    if isinstance(article_id, str):
        article_id = ObjectId(article_id)

    article = await article_collection.find_one({"_id": article_id})
    if article:
        article['_id'] = str(article['_id'])
    return article