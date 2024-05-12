from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from injector import inject
from langchain_community.document_loaders import PyPDFLoader

from src.connectedpapersextractor import Article
from src.connectedpapersextractor.article import Documents


@inject
class TextSplitterService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def split_text_to_documents(self, summary: Article) -> Documents:
        pass


class DefaultTextSplitterService(TextSplitterService):
    def split_text_to_documents(self, summary: Article) -> Documents:
        loader = PyPDFLoader(str(summary.file_path))
        documents = loader.load()
        for document in documents:
            document.metadata["source"] = str(summary.file_path)
        return documents


default_text_splitter = DefaultTextSplitterService()
