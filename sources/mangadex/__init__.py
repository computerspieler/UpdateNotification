from datetime import datetime
import logging
import re
import requests
from pydantic import ValidationError
from typing import Optional, Callable

from common import Notification, NotificationLevel
from sources import InputSource

from sources.mangadex.manga_feed import Model as MangaFeed
from sources.mangadex.manga_feed import Datum

_REGEX = re.compile(r"https://mangadex.org/title/([0-9a-f\-]+)/([^/]+)")
BASE_URL = "https://api.mangadex.org"
INTERESTING_LANGUAGES = ["en"]

BODY_FORMAT = """New chapter: {chapter} {chapterName}
Published on {date}"""

@InputSource
class Mangadex:
    def is_url_valid(url: str) -> bool:
        return bool(_REGEX.fullmatch(url))

    def get_name(url: str) -> str:
        grps  =_REGEX.fullmatch(url)
        assert grps is not None
        return grps.group(2)
    
    def get_release(url: str, last_update: datetime) -> Optional[Notification]:
        grps  =_REGEX.fullmatch(url)
        assert grps is not None
        manga_id = str(grps.group(1))

        resp = requests.get(
            f"{BASE_URL}/manga/{manga_id}/feed",
            params = {
                "translatedLanguage[]": INTERESTING_LANGUAGES,
                "order[publishAt]": "desc"
            })
        if resp.status_code != 200:
            logging.warning(f"Received an error {resp.status_code}: {resp.body}")
            return None
        
        try:
            feed: MangaFeed = MangaFeed.model_validate_json(resp.content.decode("utf-8"))
            releases = [
                r for r in feed.data
                if r.attributes.publishAt >= last_update
            ]
            if len(releases) == 0:
                logging.warning("No new releases")
                return None
            
            release: Datum = sorted(
                releases,
                key = lambda x: x.attributes.publishAt
            )[-1]
            return Notification(
                title = "",
                body=BODY_FORMAT.format(
                    chapter = release.attributes.chapter,
                    chapterName = f"({release.attributes.title})" if release.attributes.title else "",
                    date = release.attributes.publishAt
                ),
                level = NotificationLevel.LOW,
                cmd_on_click =
                    ["/bin/sh", "-c", "firefox", f"https://mangadex.org/chapter/{release.id}"]
            )
        except ValidationError as e:
            logging.warning(e)
            return None
