from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app import redis


@dataclass
class Link:
    name: str
    description: str
    url: str
    created_date: int
    modified_date: int
    id: int = 0

    @staticmethod
    def get_links() -> list[dict[str, Any]]:
        link_ids = redis.zrevrange("posts", 0, -1)
        links = []

        # get all data based on ids in reverse order
        for link_id in link_ids:
            link = redis.hgetall(f"link:{link_id}")
            links.append(link)

        return links

    @staticmethod
    def create_link(new_link: Link) -> dict[str, Any]:
        redis_pipeline = redis.pipeline()
        redis_pipeline.multi()

        # prepare link id to be stored in redis
        next_link_id = redis.incr("link_id")
        new_link.id = next_link_id

        redis_pipeline.hset(f"link:{next_link_id}", mapping=vars(new_link))
        redis_pipeline.zadd("posts", {next_link_id, new_link.created_date})
        redis_pipeline.execute()

        return new_link

    @staticmethod
    def update_link(new_data: Link, id: str) -> dict[str, Any]:
        redis_pipeline = redis.pipeline()
        redis_pipeline.multi()

        # update one data
        redis_pipeline.hset(f"link:{id}", mapping=vars(new_data))
        redis_pipeline.execute()

        return new_data

    @staticmethod
    def delete_link(id: str) -> None:
        redis_pipeline = redis.pipeline()
        redis_pipeline.multi()

        # delete one data
        redis_pipeline.hdel(f"link:{id}")
