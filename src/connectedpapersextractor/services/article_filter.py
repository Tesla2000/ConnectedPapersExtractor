from __future__ import annotations

from injector import inject

from src.connectedpapersextractor.article import Articles


@inject
class ArticleFilterService:

    def __init__(self):
        pass

    def filter(self, summaries: Articles) -> Articles:
        return summaries
