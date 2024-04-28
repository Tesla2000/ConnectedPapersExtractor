from abc import ABC, abstractmethod

from langchain_core.documents import Document

from . import PdfSummary


class MainPartsExtractor(ABC):
    @abstractmethod
    def extract(self, summary: PdfSummary) -> list[Document]:
        pass


class _DefaultExtractor(MainPartsExtractor):
    def extract(self, summary: PdfSummary) -> list[Document]:
        return summary.docs
