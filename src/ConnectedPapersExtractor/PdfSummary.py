import os
from dataclasses import dataclass, field
from pathlib import Path

from PyPDF2.errors import PdfReadError
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.documents import Document
from PyPDF2 import PdfReader


@dataclass
class PdfSummary:
    file_path: Path
    year: int = None
    citations: int = None
    _n_pages: int = field(init=False, default=None)

    def extract_documents(self) -> list[Document]:
        loader = PyPDFLoader(str(self.file_path))
        documents = loader.load()
        for document in documents:
            document.metadata["source"] = str(self.file_path)
        return documents

    def is_valid(self) -> bool:
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
                self._n_pages = len(PdfReader(io).pages)
            finally:
                io.close()
        return self._n_pages


PdfSummaries = list[PdfSummary]
