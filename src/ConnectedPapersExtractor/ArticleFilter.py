from abc import ABC, abstractmethod

from .PdfSummary import PdfSummary


class ArticleFilter(ABC):
    @abstractmethod
    def filter(self, summaries: list[PdfSummary]) -> list[PdfSummary]:
        pass
