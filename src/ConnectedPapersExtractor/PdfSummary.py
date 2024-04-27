import os
from dataclasses import dataclass, field
from pathlib import Path

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.documents import Document
from pypdf.errors import PdfStreamError


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
        try:
            PyPDFLoader(str(self.file_path)).load()
        except PdfStreamError:
            os.remove(str(self.file_path.absolute()))
            return False
        return True

    @property
    def n_pages(self) -> int:
        if self._n_pages is None:
            loader = PyPDFLoader(str(self.file_path))
            self._n_pages = len(loader.load_and_split())
        return self._n_pages
