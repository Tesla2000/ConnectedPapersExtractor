from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from injector import inject

from src.connectedpapersextractor.article import Articles


@inject
class ArticleFilterService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def filter(self, summaries: Articles) -> Articles:
        pass


class DefaultArticleFilterService(ArticleFilterService):
    def filter(self, summaries: Articles) -> Articles:
        return summaries


default_article_filter = DefaultArticleFilterService()
