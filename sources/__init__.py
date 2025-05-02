URL_VALIDATOR = {}
URL_NAME_EXTRACTOR = {}
RELEASE_RETRIEVER = {}

def InputSource(cls: type):
    typeName = cls.__name__.upper()

    URL_VALIDATOR[typeName] = cls.is_url_valid
    URL_NAME_EXTRACTOR[typeName] = cls.get_name
    RELEASE_RETRIEVER[typeName] = cls.get_release

from .github import Github