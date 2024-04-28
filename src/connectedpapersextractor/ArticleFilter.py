from abc import ABC, abstractmethod

from .PdfSummary import PdfSummaries


class ArticleFilter(ABC):
    @abstractmethod
    def filter(self, summaries: PdfSummaries) -> PdfSummaries:
        pass
