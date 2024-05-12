from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.connectedpapersextractor.article import Articles


class ArticleFilterService(ABC):
    @abstractmethod
    def filter(self, summaries: Articles) -> Articles:
        pass


class DefaultArticleFilterService(ArticleFilterService):
    def filter(self, summaries: Articles) -> Articles:
        return summaries


default_article_filter = DefaultArticleFilterService()
