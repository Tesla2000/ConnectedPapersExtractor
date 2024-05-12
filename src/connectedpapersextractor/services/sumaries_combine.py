from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from operator import attrgetter

from injector import inject

from src.connectedpapersextractor.article import Articles


@inject
class SummariesCombineService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def combine(self, articles_with_summaries: Articles) -> str:
        pass


class DefaultSummariesCombineService(SummariesCombineService):
    def combine(self, articles_with_summaries: Articles) -> str:
        return "\n\n".join(
            map(": ".join,
                map(attrgetter("title", "text_summary"),
                    articles_with_summaries),
                )
            )


default_summaries_combine = DefaultSummariesCombineService()
