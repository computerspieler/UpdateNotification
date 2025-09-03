from typing import Optional, Callable
from datetime import datetime

from common import Notification

URL_VALIDATOR: dict[str, Callable[[str], bool]] = {}
URL_NAME_EXTRACTOR: dict[str, Callable[[str], str]] = {}
RELEASE_RETRIEVER: dict[str, Callable[[str, datetime], Optional[Notification]]] = {}

def InputSource(cls: type):
    typeName = cls.__name__.upper()

    URL_VALIDATOR[typeName] = cls.is_url_valid
    URL_NAME_EXTRACTOR[typeName] = cls.get_name
    RELEASE_RETRIEVER[typeName] = cls.get_release

from .github import Github
from .mangadex import Mangadex
