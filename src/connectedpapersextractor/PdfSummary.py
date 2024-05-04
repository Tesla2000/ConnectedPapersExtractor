import os
from dataclasses import dataclass, field
from pathlib import Path

from PyPDF2 import PdfReader, PageObject
from PyPDF2.errors import PdfReadError
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.documents import Document


@dataclass
class PdfSummary:
    file_path: Path
    download_link: str = None
    title: str = None
    year: int = None
    citations: int = None
    _n_pages: int = field(init=False, default=None)
    _n_words: int = field(init=False, default=None)
    docs: list[Document] = field(init=False, default=None)
    text_summary: list[Document] = field(init=False, default=None)

    def extract_documents(self) -> list[Document]:
        loader = PyPDFLoader(str(self.file_path))
        documents = loader.load()
        for document in documents:
            document.metadata["source"] = str(self.file_path)
        self.docs = documents
        return documents

    def is_valid(self) -> bool:
        if not self.file_path.exists():
            return False
        io = self.file_path.open("rb")
        try:
            PdfReader(io)
        except PdfReadError:
            io.close()
            os.remove(str(self.file_path.absolute()))
            return False
        return True

    @property
    def n_pages(self) -> int:
        io = self.file_path.open("rb")
        if self._n_pages is None:
            try:
                reader = PdfReader(io)
                self._n_pages = len(reader.pages)
                self._n_words = sum(
                    map(len, map(str.split, map(PageObject.extract_text, reader.pages)))
                )
            finally:
                io.close()
        return self._n_pages

    @property
    def n_words(self) -> int:
        io = self.file_path.open("rb")
        if self._n_words is None:
            try:
                reader = PdfReader(io)
                self._n_pages = len(reader.pages)
                self._n_words = sum(
                    map(len, map(str.split, map(PageObject.extract_text, reader.pages)))
                )
            finally:
                io.close()
        return self._n_words

    def __eq__(self, other):
        if not isinstance(other, PdfSummary):
            return False
        return self.file_path == other.file_path


PdfSummaries = list[PdfSummary]
